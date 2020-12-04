# import wiringpi as wp
import numpy as np
import time

class Reflection():
    def __init__(self, pinLed_X, pinLed_Y):
        self.pinLed_X = pinLed_X
        self.pinLed_Y = pinLed_Y
        self.dx = 1
        self.dy = 1
        self.matrix = np.zeros((len(pinLed_Y), len(pinLed_X)))
        self.w = len(pinLed_X)
        self.h = len(pinLed_Y)

        # wp.wiringPiSetupSys()
        # for led in pinLed_X+pinLed_Y:
        #     wp.pinMode(led, wp.GPIO.OUTPUT)


    def lightup(self, matrix, sec):
        start_time = time.time()

        try:
            while time.time() - start_time > sec:
                for idx, row in enumerate(matrix):
                    for idy, flag in enumerate(row):
                        if flag:
                            wp.digitalWrite(self.pinLed_X[idx], wp.GPIO.HIGH)
                            wp.digitalWrite(self.pinLed_Y[idy], wp.GPIO.LOW)
                            time.sleep(0.01)
                            wp.digitalWrite(self.pinLed_X[idx], wp.GPIO.LOW)
                            wp.digitalWrite(self.pinLed_Y[idy], wp.GPIO.LOW)
        finally:
            for led_x in self.pinLed_X:
                wp.digitalWrite(led_x, wp.GPIO.LOW)
            for led_y in self.pinLed_Y:
                wp.digitalWrite(led_y, wp.GPIO.LOW)


    def initialize_matrix(self, x_init, y_init):
        self.matrix[y_init][x_init] = 1
        self._ball_x = x_init
        self._ball_y = y_init

    def nextmatrix(self):
        if self._ball_x <= 0 or self._ball_x >= self.w-1:
            self.dx *= -1
        if self._ball_y <= 0 or self._ball_y >= self.h-2:
            self.dy *= -1

        self._ball_x += self.dx
        self._ball_y += self.dy


        self.matrix = np.zeros((self.h, self.w))
        self.matrix[self._ball_y][self._ball_x] = 1

    # def init_bar(self, bar_length):


if __name__ == "__main__":
    ref = Reflection(range(9), range(9))
    ref.initialize_matrix(3, 2)
    for _ in range(100):
        ref.nextmatrix()
        
        print(f"\r{ref.matrix}\033[8A", end="")
        time.sleep(0.1)