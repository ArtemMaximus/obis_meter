import argparse
from .neva_mt_counter.library.NevaMt3xx import NevaMt3xx_com

class NevaCommands:
    def __init__(self, port):
        self.counter = NevaMt3xx_com(port=port)

    def read_parameter(self, obis_code):
        """Чтение параметра по OBIS-коду."""
        try:
            # Подключение и авторизация
            company, device = self.counter.connect()
            if not company or not device:
                raise Exception("Failed to connect to the counter")

            # Отправка команды
            command = ('R1', f"{obis_code}()")
            self.counter.send(self.counter.Command(command[0], command[1]))
            response = self.counter.receive()

            # Обработка ответа
            if response.is_message:
                return response.data.strip('()')
            else:
                raise Exception("Invalid response from the counter")
        except Exception as e:
            print(f"Error reading parameter: {e}")
            return None

    def read_all_parameters(self):
        """Чтение всех необходимых параметров."""
        obis_codes = {
            "voltage_phase_a": "010902FF",
            "voltage_phase_b": "020902FF",
            "voltage_phase_c": "030902FF",
            "current_phase_a": "040902FF",
            "current_phase_b": "050902FF",
            "current_phase_c": "060902FF",
            "frequency": "070902FF",
            "battery_level": "080902FF",
            "energy_t1": "090902FF",
            "energy_t2": "100902FF",
            "date_time": "000902FF",
        }

        results = {}
        for key, obis_code in obis_codes.items():
            value = self.read_parameter(obis_code)
            results[key] = float(value) if value and value.replace('.', '', 1).isdigit() else value

        return results