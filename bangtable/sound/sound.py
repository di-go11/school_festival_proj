# import pyaudio
import numpy as np
import wave
import pyaudio
import time
import sounddevice as sd
from pydub import AudioSegment


class Sound:
    count_down_sound_path = "./soundfile/button17.wav"
    fight_sound_path = "./soundfile/fight.wav"
    five_path = "./soundfile/count_voice/five.wav"
    four_path = "./soundfile/count_voice/four.wav"
    three_path = "./soundfile/count_voice/three.wav"
    two_path = "./soundfile/count_voice/two.wav"
    one_path = "./soundfile/count_voice/one.wav"

    def __init__(self,device) -> None:
        pass

    def main(self) -> None:
        pass

    def countdown(self) -> None:
        # self.file_path = self.count_down_sound_path
        rest_time = 5
        start_time = current_time = time.time()
        # print(start_time)
        while True:
            if (current_time + rest_time) >= start_time:
                print(rest_time)
                # self.play_soundfile()
                if rest_time == 5:
                    rest_time -= 1
                    self.file_path = self.five_path
                    self.play_soundfile()
                elif rest_time == 4:
                    self.file_path = self.four_path
                    self.play_soundfile()
                    rest_time -= 1
                elif rest_time == 3:
                    self.file_path = self.three_path
                    self.play_soundfile()
                    rest_time -= 1
                elif rest_time == 2:
                    self.file_path = self.two_path
                    self.play_soundfile()
                    rest_time -= 1
                elif rest_time == 1:
                    self.file_path = self.one_path
                    self.play_soundfile()
                    rest_time -= 1
                elif rest_time == 0:
                    break

    def bang(self) -> None:
        self.file_path = self.fight_sound_path
        self.play_soundfile()
    
    # def result(self) -> None:

    def play_soundfile(self,device) -> None:
        # wavファイルを開く
        wf = wave.open(self.file_path, "rb")
        # wavファイルのデータを読み込む
        p_conf = pyaudio.PyAudio()
        # 利用可能なデバイスを一覧表示
        # ストリーム開く
        stream = p_conf.open(
            format=p_conf.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            output_device_index=device
        )
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        stream.close()
        p_conf.terminate()


if __name__ == "__main__":
    print(sd.query_devices())
    sound = Sound()
    sound.countdown()
    sound.bang()
