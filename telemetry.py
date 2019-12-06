import csv
import time
from datetime import datetime
from gdpr_prov_decorators import config, init_db, GDPR_API, init, combine_personal_data, GDPRProv

config['DATABASE_TYPE'] = GDPR_API['LOCAL_SQLITE']
init_db({'DB_LOCAL': 'gdpr-prov.db.sqlite'})
controller = init('Aliens')

DATA_TELEMETRY_MOVE  = 'telemetry_move.csv'
DATA_TELEMETRY_SCORE = 'telemetry_score.csv'
DATA_TELEMETRY_SHOT  = 'telemetry_shot.csv'
DATA_TELEMETRY_KILL  = 'telemetry_kill.csv'

import uuid

class Telemetry:
    LAST_MOVE = None

    class __Telemetry:
        def __init__(self, player_name, consent):
            self.CURRENT_PLAYER = player_name if consent else str(uuid.uuid4())
            self.GIVE_CONSENT   = consent
            # if consent:
            #     ### Subject
            #     self.subject = GDPRProv.read_subject(player_name)
            #     if self.subject is None or len(self.subject) == 0:
            #         self.subject =  GDPRProv.create_subject(player_name)
            #     else:
            #         self.subject = self.subject[0]

            #     import pdb; pdb.set_trace()
            #     ### ConsentRequest
            #     self.consent_request = GDPRProv.read_consent_request_by_subject(self.subject)
            #     if self.consent_request is None or len(self.consent_request) == 0:
            #         self.consent_request = GDPRProv.create_consent_request('telemetry', self.subject)
            #     else:
            #         self.consent_request = [cr for cr in self.consent_request if cr['name'] == 'telemetry']
            #         if len(self.consent_request) == 0:
            #             self.consent_request = GDPRProv.create_consent_request('telemetry', self.subject)
            #         else:
            #             self.consent_request = self.consent_request[0]

            #     ### Consent
            #     self.consent = GDPRProv.read_consents_by_name_and_subject('telemetry', self.subject)
            #     if self.consent is None or len(self.consent) == 0:
            #         self.consent = GDPRProv.create_consent('telemetry', [self.consent_request], controller)
            #     else:
            #         self.consent = self.consent[0]

            #     ### Consent
            #     self.personal_data = GDPRProv.read_personal_data_by_subject(self.subject)
            #     if self.personal_data is None or len(self.consent) == 0:
            #         self.personal_data = GDPRProv.create_personal_data('telemetry', self.personal_data, self.subject)
            #     else:
            #         self.personal_data = [pd for pd in self.personal_data if pd['name'] == 'telemetry']
            #         if len(self.personal_data) == 0:
            #             self.personal_data = GDPRProv.create_personal_data('telemetry', self.personal_data, self.subject)
            #         else:
            #             self.personal_data = self.personal_data[0]

        def __str__(self):
            return repr(self) + self.player_name
    instance = None
    def __init__(self, player_name, consent):

        if not Telemetry.instance:
            Telemetry.instance = Telemetry.__Telemetry(player_name, consent)
        else:
            Telemetry.instance.player_name = player_name
    def __getattr__(self, name):
        return getattr(self.instance, name)
        
# DATA_TELEMETRY_MOVE  = 'telemetry_move.csv'
# DATA_TELEMETRY_SCORE = 'telemetry_score.csv'
# DATA_TELEMETRY_SHOT  = 'telemetry_shot.csv'
# DATA_TELEMETRY_KILL  = 'telemetry_kill.csv'

    @combine_personal_data
    def save(params):
        # row = [str(i) for i in row]
        data      = {k: params['data'][k] for k in params['data'] if k is not 'file_name'}
        row       = list(data.values())
        file_name = params['data']['file_name']

        row.append(datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%f'))

        with open(file_name, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        return data

    def collect_telemetry_on_move(function):
        def wrapper(self, direction):
            if direction != Telemetry.LAST_MOVE:
                Telemetry.LAST_MOVE = direction
                # Telemetry.instance.CURRENT_PLAYER = self.player_name
                
                params = {
                    'data': {
                        'player_name': Telemetry.instance.CURRENT_PLAYER, 
                        'direction':   direction,
                        'file_name':   DATA_TELEMETRY_MOVE
                    },
                    'meta': {
                        'gdpr_data': {
                            'controller': controller,
                            'subject_name': Telemetry.instance.CURRENT_PLAYER,
                            'process': 'combine',
                            'personal_data': ['player_name'],
                            'request': {
                                'consent': {
                                    'combine': ['player_name'] if Telemetry.instance.GIVE_CONSENT else []
                                }
                            }
                        }
                    }
                }

                Telemetry.save(params)

            result = function(self, direction)
            return result

        return wrapper
        
    def collect_telemetry_score(function):
        def wrapper(self):
            result = function(self)

            params = {
                'data': {
                    'player_name': Telemetry.instance.CURRENT_PLAYER, 
                    'lastscore':   self.lastscore,
                    'file_name':   DATA_TELEMETRY_SCORE
                },
                'meta': {
                    'gdpr_data': {
                        'controller': controller,
                        'subject_name': Telemetry.instance.CURRENT_PLAYER,
                        'process': 'combine',
                        'personal_data': ['player_name'],
                        'request': {
                            'consent': {
                                'combine': ['player_name'] if Telemetry.instance.GIVE_CONSENT else []
                            }
                        }
                    }
                }
            }

            Telemetry.save(params)
            return result
        return wrapper

    def collect_telemetry_shot(function):
        def wrapper(self,  pos):
            result = function(self, pos)

            params = {
                'data': {
                    'player_name': Telemetry.instance.CURRENT_PLAYER, 
                    'position':    pos,
                    'file_name':   DATA_TELEMETRY_SHOT
                },
                'meta': {
                    'gdpr_data': {
                        'controller': controller,
                        'subject_name': Telemetry.instance.CURRENT_PLAYER,
                        'process': 'combine',
                        'personal_data': ['player_name'],
                        'request': {
                            'consent': {
                                'combine': ['player_name'] if Telemetry.instance.GIVE_CONSENT else []
                            }
                        }
                    }
                }
            }

            Telemetry.save(params)
            return result
        return wrapper

    def collect_telemetry_kill(function):
        def wrapper(self):
            result = function(self)

            params = {
                'data': {
                    'player_name': Telemetry.instance.CURRENT_PLAYER, 
                    'file_name':   DATA_TELEMETRY_KILL
                },
                'meta': {
                    'gdpr_data': {
                        'controller': controller,
                        'subject_name': Telemetry.instance.CURRENT_PLAYER,
                        'process': 'combine',
                        'personal_data': ['player_name'],
                        'request': {
                            'consent': {
                                'combine': ['player_name'] if Telemetry.instance.GIVE_CONSENT else []
                            }
                        }
                    }
                }
            }

            Telemetry.save(params)
            return result
        return wrapper