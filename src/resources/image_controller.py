from flask_restful import Resource
from src.mongoDB.models.signal import Signal
import neurokit2 as nk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Esta clase hace el procesamiento de sañales
class AnalisisSignal(Resource):
    def get(self, name):
        if name == "sana":
            # hace una consulta en el esquema Signal, y obtiene todos los campos asociados con el nombre ingresado
            signal = Signal.objects.get(name=name).to_json()
            datos_cargados = pd.read_json(signal)
            matriz_numpy = datos_cargados.to_numpy()
            matriz_datos = matriz_numpy[:, 2:4]
            panda = np.append(matriz_datos, 0)
            ySana_4000 = panda[1:4000]
            # print("Signal Pandas", ySana_4000)
            longitud_senial = len(ySana_4000)
            tiempo_ySana = list(range(1, longitud_senial + 1))
            # genera la imagen de la señal recortada
            plt.plot(tiempo_ySana, ySana_4000, color='red')
            plt.xlabel('Tiempo (ms)')
            plt.ylabel('Amplitud (mV)')
            plt.title("Señal original recortada")
            plt.grid()
            plt.savefig('./images/sana/signal_recortada.png')
            plt.close()

            # Correccion de desplazamiento de línea de base
            # Normalizar los datos entre 0 y 1
            minYS = min(ySana_4000)
            maxYS = max(ySana_4000)
            ySanaNorm = (ySana_4000 - minYS) / (maxYS - minYS)
            plt.plot(tiempo_ySana, ySanaNorm)
            plt.xlabel('Tiempo (ms)')
            plt.ylabel('Amplitud (mV)')
            plt.title("Señal Original Centrada")
            plt.grid()
            plt.savefig('./images/sana/signal_centrada.png')
            plt.close()

            # ELIMINACION DE RUIDO
            import scipy.signal as ss

            # FILTRO DE ELIMINACION DE RUIDO
            # Filtro de Savitzky–Golay
            # polinomio de orden 1 ventana 23
            orden = 1
            ventana = 23
            yhat = ss.savgol_filter(ySanaNorm, ventana, orden)
            plt.plot(tiempo_ySana, yhat, color='red')
            plt.xlabel('Tiempo (ms)')
            plt.ylabel('Amplitud (mV)')
            plt.title("Señal eliminada el ruido ")
            plt.grid()
            plt.savefig('./images/sana/signal_sin_ruido.png')
            plt.close()

            # DATOS DE TENDENCIA CORRECCION LINEA BASE
            # La señal  anterior muestra un cambio de línea base y, por lo tanto, no representa la amplitud real.
            # Para eliminar la tendencia, ajuste un polinomio de orden bajo a la señal y use el polinomio para detenerla.
            polynomial_fit_coeff = np.polyfit(tiempo_ySana, yhat, 6)
            lon_intrp_2 = np.polyval(polynomial_fit_coeff, tiempo_ySana)
            ECG_datos = (yhat - lon_intrp_2)

            N1 = len(yhat)
            intervalo = list(range(0, longitud_senial))
            frecuencia_muestreo = 1000
            t2 = [x / frecuencia_muestreo for x in intervalo]

            plt.plot(t2, ECG_datos, c="r")
            plt.title("Corrección desplazamiento línea base ")
            plt.xlabel('Tiempo (ms)')
            plt.ylabel('Amplitud (mV)')
            plt.grid()
            plt.savefig('./images/sana/signal_linea_base.png')
            plt.close()

            # BUSQUEDA DE PICOS  neurokit2
            ECG_signal, info = nk.ecg_process(ECG_datos, sampling_rate=1000)
            # Visualise the processing
            nk.ecg_plot(ECG_signal, sampling_rate=1000)
            plt.grid()
            plt.savefig('./images/sana/signal_varios.png')
            plt.close()

            # NEUROKIT - ANALISIS SEGMENTO DE SEÑAL
            signal_clean = nk.ecg_clean(ECG_datos, sampling_rate=1000, method='neurokit')
            _, rpeaks = nk.ecg_peaks(signal_clean, sampling_rate=1000, method='neurokit')

            # NEUROKIT - DELINEAR
            signal, waves = nk.ecg_delineate(signal_clean, rpeaks, sampling_rate=1000, method="dwt", show=True,
                                             show_type='all')
            nk.events_plot(rpeaks['ECG_R_Peaks'], signal_clean)
            plt.xlabel('Tiempo (ms)')
            plt.ylabel('Amplitud (mV)')
            # plt.axhline(0.02, color='black', xmax=1)
            plt.savefig('./images/sana/signal_segmentos.png')
            plt.close()

            # NEUROKIT - Delineate the ECG signal and visualizing all peaks of ECG complexes
            _, waves_peak = nk.ecg_delineate(signal_clean, rpeaks, sampling_rate=1000, show=True, show_type='peaks')
            plt.xlabel('Tiempo (ms)')
            plt.ylabel('Amplitud (mV)')
            plt.grid()
            plt.title("Señal Sana ECG")
            plt.savefig('./images/sana/signal_peaks.png')
            plt.close()

            import pyrebase
            # archivo  de configuracion de firebase storage
            config = {
                "apiKey": "AIzaSyCs7nFu23KAfclhb4DDDKXG2_10No2Dz8A",
                "authDomain": "gestor-ecg.firebaseapp.com",
                "databaseURL": "https://gestor-ecg.firebaseio.com",
                "projectId": "gestor-ecg",
                "storageBucket": "gestor-ecg.appspot.com",
                "messagingSenderId": "100496575902",
                "appId": "1:100496575902:web:c4becda6bead11a7feda8f",
                "measurementId": "G-HMZGXG96PQ"
            }

            # inicializa firebase  storage
            firestore = pyrebase.initialize_app(config)
            storage = firestore.storage()

            # GUARDA IMAGENES EN FIREBSASE STORAGE
            # Señal Recortada - ruta local
            path_local_signal_recortada = "./images/sana/signal_recortada.png"
            # ruta en firebase storage
            path_on_cloud_signal_recortada = "images/sana/signal_recortada.png"
            # guarda la imagen en firebase y revice de parametro la ruta local
            storage.child(path_on_cloud_signal_recortada).put(path_local_signal_recortada)

            # download
            # storage.child(path_on_cloud).download(path="./", filename="hola.jpg")

            # Señal centrada - ruta local
            path_local_centrada = "./images/sana/signal_centrada.png"
            # ruta en firebase storage
            path_on_cloud_signal_centrada = "images/sana/signal_centrada.png"
            # guarda la imagen en firebase y revice de parametro la ruta local
            storage.child(path_on_cloud_signal_centrada).put(path_local_centrada)

            # Señal sin ruido - ruta local
            path_local_sin_ruido = "./images/sana/signal_sin_ruido.png"
            # ruta en firebase storage
            p_c_signal_sin_ruido = "images/sana/signal_sin_ruido.png"
            # guarda la imagen en firebase y revice de parametro la ruta local
            storage.child(p_c_signal_sin_ruido).put(path_local_sin_ruido)

            # GUARDAR DATOS DE TENDENCIA CORRECCION LINEA BASE
            path_local_signal_linea_base = "./images/sana/signal_linea_base.png"
            # ruta en firebase storage
            p_c_signal_signal_linea_base = "images/sana/signal_linea_base.png"
            # guarda la imagen en firebase y revice de parametro la ruta local
            storage.child(p_c_signal_signal_linea_base).put(path_local_signal_linea_base)

            # BUSQUEDA DE PICOS  kit Process it
            path_local_signal_varios = "./images/sana/signal_varios.png"
            # ruta en firebase storage
            p_c_signal_signal_varios = "images/sana/signal_varios.png"
            # guarda la imagen en firebase y revice de parametro la ruta local
            storage.child(p_c_signal_signal_varios).put(path_local_signal_varios)

            # NEUROKIT - ANALISIS SEGMENTO DE SEÑAL
            # plt.savefig('./images/signal_segmentos.png')
            path_local_signal_segmentos = "./images/sana/signal_segmentos.png"
            # ruta en firebase storage
            p_c_signal_signal_segmentos = "images/sana/signal_segmentos.png"
            # guarda la imagen en firebase y revice de parametro la ruta local
            storage.child(p_c_signal_signal_segmentos).put(path_local_signal_segmentos)

            # NEUROKIT - Delineate the ECG signal and visualizing all peaks of ECG complexes
            # plt.savefig('./images/signal_peaks.png')
            path_local_signal_peaks = "./images/sana/signal_peaks.png"
            # ruta en firebase storage
            p_c_signal_signal_peaks = "images/sana/signal_peaks.png"
            # guarda la imagen en firebase y revice de parametro la ruta local
            storage.child(p_c_signal_signal_peaks).put(path_local_signal_peaks)

            # print("Señal Sana")
            return {"ok": 200}
        else:
            if name == "enferma":

                # consulta en el esquema Signal, y obtiene todos los campos asociados con el nombre ingresado
                signal = Signal.objects.get(name=name).to_json()
                datos_cargados = pd.read_json(signal)
                matriz_numpy = datos_cargados.to_numpy()
                matriz_datos = matriz_numpy[:, 2:4]
                panda = np.append(matriz_datos, 0)
                ySana_4000 = panda[1:4000]
                longitud_senial = len(ySana_4000)
                tiempo_ySana = list(range(1, longitud_senial + 1))
                # genera la imagen de la señal recortada
                plt.plot(tiempo_ySana, ySana_4000, color='red')
                plt.xlabel('Tiempo (ms)')
                plt.ylabel('Amplitud (mV)')
                plt.title("Señal original recortada")
                plt.grid()
                plt.savefig('./images/enferma/signal_recortada.png')
                plt.close()

                # Correccion de desplazamiento de línea de base
                # Normalizar los datos entre 0 y 1
                minYS = min(ySana_4000)
                maxYS = max(ySana_4000)
                ySanaNorm = (ySana_4000 - minYS) / (maxYS - minYS)
                plt.plot(tiempo_ySana, ySanaNorm)
                plt.xlabel('Tiempo (ms)')
                plt.ylabel('Amplitud (mV)')
                plt.title("Señal Original Centrada")
                plt.grid()
                plt.savefig('./images/enferma/signal_centrada.png')
                plt.close()

                # ELIMINACION DE RUIDO
                import scipy.signal as ss

                # FILTRO DE ELIMINACION DE RUIDO
                # Filtro de Savitzky–Golay
                # polinomio de orden 1 ventana 23
                orden = 1
                ventana = 23
                yhat = ss.savgol_filter(ySanaNorm, ventana, orden)
                plt.plot(tiempo_ySana, yhat, color='red')
                plt.xlabel('Tiempo (ms)')
                plt.ylabel('Amplitud (mV)')
                plt.title("Señal eliminada el ruido ")
                plt.grid()
                plt.savefig('./images/enferma/signal_sin_ruido.png')
                plt.close()

                # DATOS DE TENDENCIA CORRECCION LINEA BASE

                polynomial_fit_coeff = np.polyfit(tiempo_ySana, yhat, 6)
                lon_intrp_2 = np.polyval(polynomial_fit_coeff, tiempo_ySana)
                ECG_datos = (yhat - lon_intrp_2)

                N1 = len(yhat)
                intervalo = list(range(0, longitud_senial))
                frecuencia_muestreo = 1000
                t2 = [x / frecuencia_muestreo for x in intervalo]

                plt.plot(t2, ECG_datos, c="r")
                plt.title("Corrección desplazamiento línea base ")
                plt.xlabel('Tiempo (ms)')
                plt.ylabel('Amplitud (mV)')
                plt.grid()
                plt.savefig('./images/enferma/signal_linea_base.png')
                plt.close()

                # BUSQUEDA DE PICOS  kit Process it
                ECG_signal, info = nk.ecg_process(ECG_datos, sampling_rate=1000)
                # Visualise the processing
                nk.ecg_plot(ECG_signal, sampling_rate=1000)
                plt.grid()
                plt.savefig('./images/enferma/signal_varios.png')
                plt.close()

                # NEUROKIT - ANALISIS SEGMENTO DE SEÑAL
                signal_clean = nk.ecg_clean(ECG_datos, sampling_rate=1000, method='neurokit')
                _, rpeaks = nk.ecg_peaks(signal_clean, sampling_rate=1000, method='neurokit')

                # NEUROKIT - DELINEAR
                signal, waves = nk.ecg_delineate(signal_clean, rpeaks, sampling_rate=1000, method="dwt", show=True,
                                                 show_type='all')
                nk.events_plot(rpeaks['ECG_R_Peaks'], signal_clean)
                plt.xlabel('Tiempo (ms)')
                plt.ylabel('Amplitud (mV)')
                # plt.axhline(0.02, color='black', xmax=1)
                plt.savefig('./images/enferma/signal_segmentos.png')
                plt.close()

                # NEUROKIT - Delineate the ECG signal and visualizing all peaks of ECG complexes
                _, waves_peak = nk.ecg_delineate(signal_clean, rpeaks, sampling_rate=1000, show=True, show_type='peaks')
                plt.xlabel('Tiempo (ms)')
                plt.ylabel('Amplitud (mV)')
                plt.grid()
                plt.title("Señal Enferma ECG")
                plt.savefig('./images/enferma/signal_peaks.png')
                plt.close()

                import pyrebase
                # archivo  de configuracion de firebase storage
                config = {
                    "apiKey": "AIzaSyCs7nFu23KAfclhb4DDDKXG2_10No2Dz8A",
                    "authDomain": "gestor-ecg.firebaseapp.com",
                    "databaseURL": "https://gestor-ecg.firebaseio.com",
                    "projectId": "gestor-ecg",
                    "storageBucket": "gestor-ecg.appspot.com",
                    "messagingSenderId": "100496575902",
                    "appId": "1:100496575902:web:c4becda6bead11a7feda8f",
                    "measurementId": "G-HMZGXG96PQ"
                }

                # inicializa firebase  storage
                firestore = pyrebase.initialize_app(config)
                storage = firestore.storage()

                # GUARDA IMAGENES EN FIREBSASE STORAGE
                # Señal Recortada - ruta local
                path_local_signal_recortada = "./images/enferma/signal_recortada.png"
                # ruta en firebase storage
                path_on_cloud_signal_recortada = "images/enferma/signal_recortada.png"
                # guarda la imagen en firebase y revice de parametro la ruta local
                storage.child(path_on_cloud_signal_recortada).put(path_local_signal_recortada)

                # download
                # storage.child(path_on_cloud).download(path="./", filename="hola.jpg")

                # Señal centrada - ruta local
                path_local_centrada = "./images/enferma/signal_centrada.png"
                # ruta en firebase storage
                path_on_cloud_signal_centrada = "images/enferma/signal_centrada.png"
                # guarda la imagen en firebase y revice de parametro la ruta local
                storage.child(path_on_cloud_signal_centrada).put(path_local_centrada)

                # Señal sin ruido - ruta local
                path_local_sin_ruido = "./images/enferma/signal_sin_ruido.png"
                # ruta en firebase storage
                p_c_signal_sin_ruido = "images/enferma/signal_sin_ruido.png"
                # guarda la imagen en firebase y revice de parametro la ruta local
                storage.child(p_c_signal_sin_ruido).put(path_local_sin_ruido)

                # GUARDAR DATOS DE TENDENCIA CORRECCION LINEA BASE
                path_local_signal_linea_base = "./images/enferma/signal_linea_base.png"
                # ruta en firebase storage
                p_c_signal_signal_linea_base = "images/enferma/signal_linea_base.png"
                # guarda la imagen en firebase y revice de parametro la ruta local
                storage.child(p_c_signal_signal_linea_base).put(path_local_signal_linea_base)

                # BUSQUEDA DE PICOS  kit Process it
                path_local_signal_varios = "./images/enferma/signal_varios.png"
                # ruta en firebase storage
                p_c_signal_signal_varios = "images/enferma/signal_varios.png"
                # guarda la imagen en firebase y revice de parametro la ruta local
                storage.child(p_c_signal_signal_varios).put(path_local_signal_varios)

                # NEUROKIT - ANALISIS SEGMENTO DE SEÑAL
                # plt.savefig('./images/signal_segmentos.png')
                path_local_signal_segmentos = "./images/enferma/signal_segmentos.png"
                # ruta en firebase storage
                p_c_signal_signal_segmentos = "images/enferma/signal_segmentos.png"
                # guarda la imagen en firebase y revice de parametro la ruta local
                storage.child(p_c_signal_signal_segmentos).put(path_local_signal_segmentos)

                # NEUROKIT - Delineate the ECG signal and visualizing all peaks of ECG complexes
                # plt.savefig('./images/signal_peaks.png')
                path_local_signal_peaks = "./images/enferma/signal_peaks.png"
                # ruta en firebase storage
                p_c_signal_signal_peaks = "images/enferma/signal_peaks.png"
                # guarda la imagen en firebase y revice de parametro la ruta local
                storage.child(p_c_signal_signal_peaks).put(path_local_signal_peaks)

            return {"ok": 200}
