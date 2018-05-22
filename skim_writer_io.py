#!/usr/bin/env python3


class Skim_writer_io:
    '''
    Handle FileIO writes, writing to files according to parameters.
    '''
    def writer(self, site: str, file_name: str) -> bool:
        try:
            import skim_controller
            base_path: str = skim_controller.SkimController().basepath
            with open(str(base_path) + str(file_name) + ".txt", "a") as file:
                file.write(str(site) + "\n")
                file.close()
            return True
        except Exception as e:
            print("Error! in Skim_writer_io.writer: " + str(e))


