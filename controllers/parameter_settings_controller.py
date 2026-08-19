from tkinter import messagebox
import os


class ParameterSettingsController():
    def __init__(self,context,db):
        self.context = context
        self.context.database_manager=db


    def save_settings(self,data):
        try:
            conn = self.context.database_manager.get_connection()
            conn.execute("BEGIN")

            self.context.parameter_repository.save_endurance_settings(conn, data)

            self.context.parameter_repository.save_line_common_settings(conn, data)

            self.context.parameter_repository.save_obc_input(conn, data)

            # self.parameter_repository.save_obc_output(conn, data)

            self.context.parameter_repository.save_hpdc_input(conn, data)

            self.context.parameter_repository.save_load_common_settings(conn, data)

            self.context.parameter_repository.save_obc_current_settings(conn,data)

            self.context.parameter_repository.save_hpdc_current_settings(conn,data)

            # self.parameter_repository.save_hpdc_load_hv(conn, data)

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Settings saved successfully."
            )

        except Exception as e:

            conn.rollback()
            print(str(e))
            messagebox.showerror(
                "Error",
                str(e)
            ) 

    def get_all_duts(self):
        conn = self.context.database_manager.get_connection()
        return self.context.parameter_repository.get_all_duts(conn)

    def delete_duts(self, dut_ids):
        conn = self.context.database_manager.get_connection()
        self.context.parameter_repository.delete_duts(conn, dut_ids)
    
    def get_all_settings(self, dut_id):

        conn = self.context.database_manager.get_connection()

        return {
            "dut":
                self.context.parameter_repository.get_dut_settings(conn, dut_id),

            "endurance":
                self.context.parameter_repository.get_endurance_settingsbyid(conn, dut_id),

            "line_common":
                self.context.parameter_repository.get_line_common(conn, dut_id),

            "obc_line_inputs":
                self.context.parameter_repository.get_obc_line_settings(conn, dut_id),

            # "hpdc_line_current":
            #     self.context.parameter_repository.get_hpdc_line_current(conn, dut_id),

            "hpdc_line_setting":
                self.context.parameter_repository.get_hpdc_line_setting(conn, dut_id),

            "load_common":
                self.context.parameter_repository.get_load_common(conn, dut_id),

            "obc_load_settings":
                self.context.parameter_repository.get_obc_current_settings(conn, dut_id),

            "hpdc_load_settings":
                self.context.parameter_repository.get_hpdc_current_settings(conn, dut_id),
        }

    def add_dut(self,values):
        try:
            print("enter add_dut in controller")
            conn = self.context.database_manager.get_connection()
            conn.execute("BEGIN")
            # instrument = InstrumentData(
            #     instrument_name=values[0],
            #     address=values[1],
            #     instrument_sno=values[2],
            #     calibration_due_date=values[3],
            #     status=values[4],
            #     channel_id=self.selected_channel_id
            # )
        

            self.context.parameter_repository.add_dut(conn,values)
            conn.commit()
            
            messagebox.showinfo(
                "Success",
                "Added new DUT successfully."
            )

        except Exception as e:

            conn.rollback()
            print(str(e))
            messagebox.showerror(
                "Error",
                str(e)
            ) 

    def edit_dut(self,values):
            try:
                print("enter edit_dut in controller")
                conn = self.context.database_manager.get_connection()
                conn.execute("BEGIN")
    
                self.context.parameter_repository.edit_dut(conn,values)
                conn.commit()
                
                messagebox.showinfo(
                    "Success",
                    "Edited DUT successfully."
                )
    
            except Exception as e:
    
                conn.rollback()
                print(str(e))
                messagebox.showerror(
                    "Error",
                    str(e)
                ) 

    

    def save_dbc_file(self, dut_id, file_path):
        conn = self.context.database_manager.get_connection()
        self.context.parameter_repository.save_dbc_file(
            conn,
            dut_id,
            os.path.basename(file_path),
            file_path
        )
        conn.commit()

    def remove_dbc_file(self, dut_id):
        conn = self.context.database_manager.get_connection()
        self.context.parameter_repository.remove_dbc_file(
            conn,
            dut_id
        )
        conn.commit()

    def get_dbc_file(self, dut_id):
        conn = self.context.database_manager.get_connection()
        return self.context.parameter_repository.get_dbc_file(
            conn,
            dut_id
        )
                
    