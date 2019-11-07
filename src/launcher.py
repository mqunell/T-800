import sys

# Windows and AWS Ubuntu paths
sys.path.append('C:\\Users\\mqune\\OneDrive\\Documents\\Code\\PycharmProjects\\T-800')
#sys.path.append('/home/ubuntu/T-800')

from src.bot import T800

bot = T800()
bot.run()