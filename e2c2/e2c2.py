import json
import subprocess
from . import GoogleSpreadsheet, Logger


class E2C2(Logger):
    CREATE_USER_ON_INSTANCE = "ssh -i {PEM_PATH} {INSTANCE} 'sudo adduser {USER} --gecos \"\" --disabled-password'"
    HOME_DIR = '/home/{USER}/'
    SSH_DIR = '/home/{USER}/.ssh'
    CREATE_DIR = """ssh -i {PEM_PATH} {INSTANCE} \
    'sudo -u {USER} mkdir -p {SSH_DIR} && \
     chmod 700 {SSH_DIR} && \
     touch {SSH_DIR}/authorized_keys && \
     chmod 600 {SSH_DIR}/authorized_keys'"""
    ADD_USER_KEY_TO_AUTHORIZED_KEYS = "ssh -i {PEM_PATH} {INSTANCE} \"sudo -u {USER} sh -c \'echo \"{USER_KEY}\" >> {SSH_DIR}/authorized_keys\'\""

    def __init__(self):
        Logger.__init__(self)

        self.spreadsheet = GoogleSpreadsheet()

        self.logger.info('Downloading spreadsheets')
        self.users = self.spreadsheet.get_users()
        self.instances = self.spreadsheet.get_instances()
        self.permissions = self.spreadsheet.get_permissions()
        self.logger.info('Spreadsheets are downloaded')

    def formatted_json(self, json_):
        return json.dumps(json_, sort_keys=True, indent=4, separators=(',', ': '))

    def get_public_key(self, user):
        self.logger.info("Get public key by %s" % user)
        return self.users[user]

    def get_host(self, instance):
        self.logger.info("Get host by %s" % instance)
        return self.instances[instance]

    def get_pem_file(self, instance):
        return instance + '.pem'

    def create_user_on_instance(self, user, instance):
        command = self.CREATE_USER_ON_INSTANCE.format(PEM_PATH=self.get_pem_file(instance),
                                                      USER=user, INSTANCE=instance)
        self.logger.debug("CREATE_USER_ON_INSTANCE:\n%s" % command)

        command = self.CREATE_DIR.format(USER=user, SSH_DIR=self.SSH_DIR.format(USER=user),
                                         PEM_PATH=self.get_pem_file(instance), INSTANCE=instance)
        self.logger.debug("CREATE_DIR:\n%s" % command)

    def add_user_key_to_instance(self, user, instance):
        self.create_user_on_instance(user, instance)

        command = self.ADD_USER_KEY_TO_AUTHORIZED_KEYS.format(USER=user, USER_KEY=self.get_public_key(user),
                                                              SSH_DIR=self.SSH_DIR.format(USER=user),
                                                              PEM_PATH=self.get_pem_file(instance), INSTANCE=instance)
        self.logger.debug("ADD_USER_KEY_TO_AUTHORIZED_KEYS:\n%s" % command)