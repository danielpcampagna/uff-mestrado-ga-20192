import csv
import time
from datetime import datetime

DATA_TELEMETRY_MOVE  = 'telemetry_move.csv'
DATA_TELEMETRY_SCORE = 'telemetry_score.csv'
DATA_TELEMETRY_SHOT  = 'telemetry_shot.csv'
DATA_TELEMETRY_KILL  = 'telemetry_kill.csv'

class Telemetry:
    LAST_MOVE = None
    CURRENT_PLAYER = None
    def save(*row, file_name):
        row = [str(i) for i in row]
        row.append(datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%f'))
        
        with open(file_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
    
    def collect_telemetry_on_move(function):
        def wrapper(self, direction):
            if direction != Telemetry.LAST_MOVE:
                Telemetry.LAST_MOVE = direction
                Telemetry.CURRENT_PLAYER = self.player_name
                Telemetry.save(Telemetry.CURRENT_PLAYER, direction, file_name=DATA_TELEMETRY_MOVE)

            result = function(self, direction)
            return result

        return wrapper
        
    def collect_telemetry_score(function):
        def wrapper(self):
            result = function(self)
            Telemetry.save(Telemetry.CURRENT_PLAYER, self.lastscore, file_name=DATA_TELEMETRY_SCORE)
            return result
        return wrapper

    def collect_telemetry_shot(function):
        def wrapper(self,  pos):
            result = function(self, pos)
            Telemetry.save(Telemetry.CURRENT_PLAYER, pos, file_name=DATA_TELEMETRY_SHOT)
            return result
        return wrapper

    def collect_telemetry_kill(function):
        def wrapper(self):
            result = function(self)
            Telemetry.save(Telemetry.CURRENT_PLAYER, file_name=DATA_TELEMETRY_KILL)
            return result
        return wrapper