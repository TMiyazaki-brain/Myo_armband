import myo
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class EmgListener(myo.DeviceListener):
    def __init__(self):
        self.emg_data = []

    def on_connected(self, event):
        print("Connected to Myo Armband")
        event.device.stream_emg(True)

    def on_emg(self, event):
        self.emg_data.append(event.emg)
        if len(self.emg_data) > 500:  # 保持するデータの最大数を制限
            self.emg_data.pop(0)

def main():
    myo.init()
    hub = myo.Hub()
    listener = EmgListener()

    fig, axs = plt.subplots(8, 1, figsize=(10, 10))  # 8つのサブプロットを作成

    def update(frame):
        if listener.emg_data:
            emg_data_np = np.array(listener.emg_data)
            for i in range(8):
                axs[i].clear()
                axs[i].plot(emg_data_np[:, i])
                axs[i].set_title(f'EMG Channel {i+1}')
                axs[i].set_ylabel('EMG Signal')
                axs[i].set_ylim([-128, 128])  # EMGデータの範囲に合わせてY軸を設定

    ani = animation.FuncAnimation(fig, update, interval=50)  # 50msごとに更新

    running = True

    def on_key(event):
        nonlocal running
        if event.key == 'q':
            running = False
            plt.close(fig)

    fig.canvas.mpl_connect('key_press_event', on_key)

    with hub.run_in_background(listener.on_event):
        try:
            print("Collecting EMG data...")
            plt.tight_layout()
            while running:
                plt.pause(0.1)
        except KeyboardInterrupt:
            pass

    print("Data collection stopped")

if __name__ == '__main__':
    main()