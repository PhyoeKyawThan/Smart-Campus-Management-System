from .models import Student, Staff, Teacher, Guest
from werkzeug.security import generate_password_hash
from .esp.track import Track
import json
import qrcode
from os import path, makedirs
from flask import current_app

class TokenGenerator(Track):
    DICT_TOKEN = ""
    QR_CODE_PATH = ""
    def generate(self, id: int) -> None:
        people = self._Track__get_object()[0]
        people = self.__get_data_by_id(id, people)
        format = self._Track__get_format(people)
        current_app.logger.info(format)
        self.DICT_TOKEN = {
            "id": id,
            "token": generate_password_hash(json.dumps(format)),
            "who": self.who,
        }
        
    def __get_data_by_id(self, id: int, object) -> object:
        return object.query.get(id)
    
    def get_qr_code(self, id: int):
        filename = self.who + "_" + str(id) + ".png"
        category_dir = current_app.config["QR_CODE_DIR"]
        if not path.exists(category_dir):
            makedirs(category_dir)
        qr_image_path = path.join(category_dir, filename)
        if path.exists(qr_image_path):
            self.QR_CODE_PATH = qr_image_path
            return qr_image_path
        try:
            qr = qrcode.make(json.dumps(self.DICT_TOKEN))
            qr.save(qr_image_path)
            self.QR_CODE_PATH = qr_image_path
            return qr_image_path
        except Exception as e:
            current_app.logger.error("QR: ", e)
            return None