from static import webColors

class Color:
    def __init__(self, color):
        color = color.strip()
        color = color.lower()

        if color[0] == "#":
            self.red, self.green, self.blue = self.convertHex(color)
            return

        if color in webColors:
            self.red, self.green, self.blue = webColors[color]
            return 

        color = color.split(",")
        if len(color) != 3:
            raise Exception("RGB values should be in this format: (RRR, GGG, BBB)")
        
        minValue = 0
        maxValue = 255
        for i in range(len(color)):
            color[i] = int(color[i].strip())
            if color[i] < minValue or color[i] > maxValue:
                raise Exception("RGB values should be between 0 - 255 (both inclusive)")

        self.red, self.green, self.blue = color

            
    def convertHex(self, hex):
        hex = hex.strip('#')
        n = len(hex) // 3
        if len(hex) == 3:
            r = int(hex[:n] * 2, 16)
            g = int(hex[n:2 * n] * 2, 16)
            b = int(hex[2 * n:3 * n] * 2, 16)
        else:
            r = int(hex[:n], 16)
            g = int(hex[n:2 * n], 16)
            b = int(hex[2 * n:3 * n], 16)
        return r, g, b
