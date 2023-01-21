import logging
import BlynkInteractions

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from MissingTokenException import MissingTokenException
from RequestException import RequestException
from Color import Color
from static import POWER_PIN, MODE_PIN, BRIGHTNESS_PIN
from static import POWER_ON, POWER_OFF, MODE_MUSIC, MODE_RGB 


class TelegramBot:
    def __init__(self, token, port):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        self.logger = logging.getLogger(__name__)
        self.command = {}
        self.authToken = {}
        self.token = token
        self.port = port


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        userId = update.message.from_user.id
        self.command[userId] = ""

        await update.message.reply_text('Hi there!')
        await help(update, context)


    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        userId = update.message.from_user.id
        self.command[userId] = ""

        await update.message.reply_text("These are the available commands")
        await update.message.reply_text(
            "/setAuthToken - Sets the device auth token (run before running any command)\n\n" +
            "/status - Checks if device is on\n\n" +
            "/on - Switch on the device\n\n" +
            "/off - Switch off the device\n\n" +
            "/rgb - Set the device to RGB mode\n\n" +
            "/music - Set the device to music mode\n\n"
            "/setColor - Sets the color of the lights if the device is in RGB mode\n\n" +
            "/setBrightness - Set the brightness of the lights" 
        )


    ######################## Commands #####################################


    async def setAuthToken(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        userId = update.message.from_user.id
        self.command[userId] = "/setAuthToken"
        await update.message.reply_text('Please send me your device\'s auth token')


    async def checkStatus(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        userId = update.message.from_user.id
        self.command[userId] = ""

        try:
            auth = self.getAuthToken(userId)
            status = BlynkInteractions.deviceStatus(auth)
            message = f"Device is {'online' if status else 'offline'}"
            await update.message.reply_text(message)
        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")


    async def switchOn(self, update, context):
        userId = update.message.from_user.id
        self.command[userId] = ""

        try:
            auth = self.getAuthToken(userId)
            BlynkInteractions.updateStream(auth, POWER_PIN, POWER_ON)
            await update.message.reply_text("Device is switched on")
        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")

            
    async def switchOff(self, update, context):
        userId = update.message.from_user.id
        self.command[userId] = ""

        try:
            auth = self.getAuthToken(userId)
            BlynkInteractions.updateStream(auth, POWER_PIN, POWER_OFF)
            await update.message.reply_text("Device is switched off")
        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")

            
    async def setRgbMode(self, update, context):
        userId = update.message.from_user.id
        self.command[userId] = ""

        isSwitchOn = await self.checkDeviceOn(userId, update)
        if not isSwitchOn:
            return
        
        try:
            auth = self.getAuthToken(userId)
            BlynkInteractions.updateStream(auth, MODE_PIN, MODE_RGB)
            await update.message.reply_text("Set to RGB mode")
        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")

   
    async def setMusicMode(self, update, context):
        userId = update.message.from_user.id
        self.command[userId] = ""
        
        isSwitchOn = await self.checkDeviceOn(userId, update)
        if not isSwitchOn:
            return

        try:
            auth = self.getAuthToken(userId)
            BlynkInteractions.updateStream(auth, MODE_PIN, MODE_MUSIC)
            await update.message.reply_text("Set to music mode")
        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")


    async def setColor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        userId = update.message.from_user.id
        self.command[userId] = ""
        
        isSwitchOn = await self.checkDeviceOn(userId, update)
        if not isSwitchOn:
            return

        isColorMode = await self.checkColorMode(userId, update)
        if not isColorMode:
            return

        self.command[userId] = "/setColor"
        await update.message.reply_text(
            'Please send me the color in one of the following format:\n\n' +
            "1) Hex code (#RRGGBB)\n\n" +
            "2) RGB values seperated by comma (RRR, GGG, BBB)\n\n" +
            "3) Name of color listed here (https://www.w3schools.com/colors/colors_names.asp)"
        )


    async def setBrightness(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        userId = update.message.from_user.id
        self.command[userId] = ""
        
        isSwitchOn = await self.checkDeviceOn(userId, update)
        if not isSwitchOn:
            return
    
        self.command[userId] = "/setBrightness"
        await update.message.reply_text('Please send me the brightness level from 0 to 255')


    async def unknown(self, update, context):
        userId = update.message.from_user.id
        if userId not in self.command:
            return await self.help(update, context)

        commandMap = {
            "/setAuthToken": self.postSetAuth,
            "/setBrightness": self.postSetBrightness,
            "/setColor": self.postSetColor
        }

        if self.command[userId] in commandMap:
            await commandMap[self.command[userId]](update)
        else:
            await update.message.reply_text("I do not understand this.")
            await self.help(update, context)


    ######################## Follow up methods #####################################


    async def postSetAuth(self, update):
        userId = update.message.from_user.id
        self.authToken[userId] = update.message.text  
        self.command[userId] = None
        await update.message.reply_text("Got it!")


    async def postSetBrightness(self, update):
        userId = update.message.from_user.id
        brightness = update.message.text  

        if not brightness.isnumeric():
            await update.message.reply_text("Brightness level should be a number between 0 to 255")
            return
        
        brightness = int(brightness)
        minValue = 0
        maxValue = 255

        if brightness < minValue or brightness > maxValue:
            await update.message.reply_text("Brightness level should be a number between 0 to 255")
            return

        try:
            auth = self.getAuthToken(userId)
            BlynkInteractions.updateStream(auth, BRIGHTNESS_PIN, brightness)
            self.command[userId] = None
            await update.message.reply_text("Brightness updated")
        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")


    async def postSetColor(self, update):
        userId = update.message.from_user.id
        try:
            color = Color(update.message.text)
        except:
            await update.message.reply_text("I do not understand the color. Please try again.")
            return
        
        try:
            auth = self.getAuthToken(userId)
            BlynkInteractions.sendColor(auth, color)
            self.command[userId] = None
            await update.message.reply_text("Updated color!")
        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")



    ######################## Helper methods #####################################


    def checkAuthToken(self, userId):
        return userId in self.authToken


    def getAuthToken(self, userId):
        if not self.checkAuthToken(userId):
            raise MissingTokenException()
        return self.authToken[userId]

    
    async def checkDeviceOn(self, userId, update):
        try:
            auth = self.getAuthToken(userId)
            status = BlynkInteractions.getPowerStatus(auth)
            
            if (status == POWER_OFF):
                await update.message.reply_text("Device need to be set to on first")
                return False
            return True

        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")
        
        return False


    async def checkColorMode(self, userId, update):
        try:
            auth = self.getAuthToken(userId)
            status = BlynkInteractions.getModeStatus(auth)
            if (status == MODE_MUSIC):
                await update.message.reply_text("Device need to be set to RGB mode first")
                return False
            return True

        except RequestException as err:
            await update.message.reply_text(err.message)
        except MissingTokenException as err:
            await update.message.reply_text("Please set an auth token using /setAuthToken")
        
        return False


    ######################## Main methods #####################################


    def run(self):
        """Start the bot."""
        # Create the Application and pass it your bot's token.
        application = Application.builder().token(self.token).build()

        # on different commands - answer in Telegram
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help))
        application.add_handler(CommandHandler("setAuthToken", self.setAuthToken))
        application.add_handler(CommandHandler("status", self.checkStatus))
        application.add_handler(CommandHandler("on", self.switchOn))
        application.add_handler(CommandHandler("off", self.switchOff))
        application.add_handler(CommandHandler("rgb", self.setRgbMode))
        application.add_handler(CommandHandler("music", self.setMusicMode))
        application.add_handler(CommandHandler("setColor", self.setColor))
        application.add_handler(CommandHandler("setBrightness", self.setBrightness))


        # on non command i.e message - echo the message on Telegram
        application.add_handler(MessageHandler(filters.TEXT, self.unknown))

        # Start the Bot
        application.run_polling()
