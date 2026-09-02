from datetime import datetime
from pathlib import Path

class EfficiencyTrendController:

    def __init__(self, view, context):

        self.view = view
        self.context = context

        self.running_duts = []

        self.cycle_data = {}

        for dut in range(1, 5):

            self.cycle_data[dut] = {
                "charging_samples": [],
                "discharging_samples": [],
                "cycles": [],
                "statistics": {}
            }
    # def start_live_plot(self, selected_duts):

    #     # Add newly started DUTs
    #     for dut in selected_duts:
    #         if isinstance(dut, str):
    #             dut = int(dut.replace("DUT", ""))
    #         print("Starting live plot for DUT:", dut)

    #         if dut not in self.running_duts:
    #             self.running_duts.append(dut)

    #     selected_duts = self.running_duts

    #     # Hide all canvases
    #     for canvas in self.view.canvas_map.values():
    #         canvas.grid_forget()

    #     count = len(selected_duts)

    #     if count == 0:
    #         return

    #     # Reset grid configuration
    #     for row in range(2):
    #         self.view.plot_frame.grid_rowconfigure(
    #             row,
    #             weight=1
    #         )

    #     for column in range(2):
    #         self.view.plot_frame.grid_columnconfigure(
    #             column,
    #             weight=1
    #         )

    #     # =========================
    #     # DUT POSITIONS
    #     # =========================

    #     if count == 1:

    #         positions = [
    #             (0, 0)
    #         ]

    #         self.view.plot_frame.grid_columnconfigure(
    #             1,
    #             weight=0
    #         )

    #     elif count == 2:

    #         positions = [
    #             (0, 0),
    #             (1, 0)
    #         ]

    #         self.view.plot_frame.grid_columnconfigure(
    #             1,
    #             weight=0
    #         )

    #     elif count == 3:

    #         positions = [
    #             (0, 0),
    #             (1, 0),
    #             (0, 1)
    #         ]

    #     else:

    #         positions = [
    #             (0, 0),
    #             (1, 0),
    #             (0, 1),
    #             (1, 1)
    #         ]

    #     # =========================
    #     # PLACE CANVASES
    #     # =========================

    #     for dut, (row, column) in zip(
    #         selected_duts,
    #         positions
    #     ):

    #         canvas = self.view.canvas_map[dut]

    #         canvas.grid(
    #             row=row,
    #             column=column,
    #             padx=10,
    #             pady=10,
    #             sticky="nsew"
    #         )

    #         # Update title
    #         canvas.delete("title")

    #         canvas.create_text(
    #             10,
    #             10,
    #             text=f"{dut}",
    #             anchor="nw",
    #             font=("Segoe UI", 12, "bold"),
    #             fill="black",
    #             tags="title"
    #         )

            # Test data
            # canvas.add_charging_points(88.2)
            # canvas.add_charging_points(89.5)
            # canvas.add_charging_points(90.8)

            # canvas.add_discharging_points(91.3)
            # canvas.add_discharging_points(89.7)
            # canvas.add_discharging_points(87.5)

    # def add_efficiency_sample(self, dut, mode, efficiency):

    #     if mode == "charging":
    #         self.cycle_data[dut]["charging_samples"].append(efficiency)

    #     else:
    #         self.cycle_data[dut]["discharging_samples"].append(efficiency)

    def start_live_plot(self, selected_duts):

        normalized_duts = []

        for dut in selected_duts:

            if isinstance(dut, str):
                dut_no = int(
                    dut.replace("DUT", "")
                )
            else:
                dut_no = int(dut)

            normalized_duts.append(
                dut_no
            )

        print(
            "Starting efficiency trend for:",
            normalized_duts
        )

        # Reset previous test data/display
        self.reset(
            normalized_duts
        )

        # Continue with your existing
        # live plotting logic here
    
    def add_efficiency_sample(self, dut, mode, efficiency):

        if mode == "charging":

            self.cycle_data[dut]["charging_samples"].append(
                float(efficiency)
            )

        elif mode == "discharging":

            self.cycle_data[dut]["discharging_samples"].append(
                float(efficiency)
            )

        else:

            print(
                f"[EFF WARNING] Ignoring sample: "
                f"DUT={dut}, MODE={mode}, EFF={efficiency}"
            )

    # def finish_cycle(self, dut):

    #     data = self.cycle_data[dut]
    #     print("Data ", data)
    #     charge = data["charging_samples"]
    #     print("Charge ",charge)
    #     discharge = data["discharging_samples"]
    #     print("discharge ",discharge)

    #     if charge:
    #         charge_avg = sum(charge) / len(charge)
    #     else:
    #         charge_avg = 0

    #     if discharge:
    #         discharge_avg = sum(discharge) / len(discharge)
    #     else:
    #         discharge_avg = 0

    #     cycle_no = len(data["cycles"]) + 1

    #     data["cycles"].append({
    #         "cycle": cycle_no,
    #         "charging_avg": charge_avg,
    #         "discharging_avg": discharge_avg
    #     })

    #     data["charging_samples"].clear()
    #     data["discharging_samples"].clear()

    #     # canvas = self.view.canvas_map[f"DUT{dut}"]
    #     canvas = self.view.canvas_map[dut]
    #     # canvas.add_cycle(
    #     #     cycle_no=cycle_no,
    #     #     charging=charge_avg,
    #     #     discharging=discharge_avg
    #     # )

    #     canvas.add_charging_points(charge_avg)
    #     canvas.add_discharging_points(discharge_avg)

    #     self.update_statistics(dut)

    def finish_cycle(self, dut):

        data = self.cycle_data[dut]

        charge = data["charging_samples"]
        discharge = data["discharging_samples"]

        # print()
        # print("====================================")
        # print(f"FINISH CYCLE - DUT {dut}")
        # print("Charging samples:", charge)
        # print("Discharging samples:", discharge)
        # print("====================================")
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "efficiency_samples.txt"

        with open(log_file, "a", encoding="utf-8") as f:

            f.write("\n")
            f.write("====================================\n")
            f.write(f"TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"FINISH CYCLE - DUT {dut}\n")
            f.write(f"Charging samples: {charge}\n")
            f.write(f"Discharging samples: {discharge}\n")
            f.write("====================================\n")

        # -----------------------------
        # Charging average
        # -----------------------------

        if charge:
            charge_avg = sum(charge) / len(charge)
        else:
            charge_avg = 0

        # -----------------------------
        # Discharging average
        # -----------------------------

        if discharge:
            discharge_avg = sum(discharge) / len(discharge)
        else:
            discharge_avg = 0

        cycle_no = len(data["cycles"]) + 1

        cycle_data = {
            "cycle": cycle_no,
            "charging_avg": charge_avg,
            "discharging_avg": discharge_avg
        }

        data["cycles"].append(cycle_data)

        print(
            f"DUT {dut} Cycle {cycle_no}: "
            f"Charging={charge_avg:.2f}, "
            f"Discharging={discharge_avg:.2f}"
        )

        # -----------------------------
        # Clear samples for next cycle
        # -----------------------------

        data["charging_samples"].clear()
        data["discharging_samples"].clear()

        # -----------------------------
        # Update graph
        # -----------------------------

        canvas = self.view.canvas_map[dut]

        canvas.add_charging_points(charge_avg)
        canvas.add_discharging_points(discharge_avg)

        # -----------------------------
        # Update statistics
        # -----------------------------

        self.update_statistics(dut)
    
    def update_statistics(self, dut):

        data = self.cycle_data[dut]

        if not data["cycles"]:
            return

        # -----------------------------
        # Charging statistics
        # -----------------------------
        charging = [
            (cycle["cycle"], cycle["charging_avg"])
            for cycle in data["cycles"]
        ]

        charge_values = [value for _, value in charging]

        print(charge_values,dut)

        charge_min = min(charging, key=lambda x: x[1])
        charge_max = max(charging, key=lambda x: x[1])
        charge_avg = sum(charge_values) / len(charge_values)



        # -----------------------------
        # Discharging statistics
        # -----------------------------
        discharging = [
            (cycle["cycle"], cycle["discharging_avg"])
            for cycle in data["cycles"]
        ]

        discharge_values = [value for _, value in discharging]

        print(discharge_values,dut)

        discharge_min = min(discharging, key=lambda x: x[1])
        discharge_max = max(discharging, key=lambda x: x[1])
        discharge_avg = sum(discharge_values) / len(discharge_values)

        # Save statistics
        data["statistics"] = {
            "charging": {
                "min": {
                    "cycle": charge_min[0],
                    "value": charge_min[1]
                },
                "max": {
                    "cycle": charge_max[0],
                    "value": charge_max[1]
                },
                "avg": charge_avg
            },
            "discharging": {
                "min": {
                    "cycle": discharge_min[0],
                    "value": discharge_min[1]
                },
                "max": {
                    "cycle": discharge_max[0],
                    "value": discharge_max[1]
                },
                "avg": discharge_avg
            }
        }
        self.view.update_efficiency_summary(
            dut,
            data["statistics"]
        )

    def reset(self, selected_duts):

        print(
            "EfficiencyTrendController.reset:",
            selected_duts
        )

        for dut in selected_duts:

            dut_no = int(dut)

            # Reset controller data
            self.cycle_data[dut_no] = {
                "charging_samples": [],
                "discharging_samples": [],
                "cycles": [],
                "statistics": {
                    "charging": {
                        "max": {
                            "value": 0,
                            "cycle": 0
                        },
                        "min": {
                            "value": 0,
                            "cycle": 0
                        },
                        "avg": 0
                    },
                    "discharging": {
                        "max": {
                            "value": 0,
                            "cycle": 0
                        },
                        "min": {
                            "value": 0,
                            "cycle": 0
                        },
                        "avg": 0
                    }
                }
            }

        # Tell VIEW to clear graph and display
        self.view.reset_display(
            selected_duts
        )
    # def reset(self, selected_duts):

    #     for dut in selected_duts:

    #         self.cycle_data[dut] = {
    #             "charging_samples": [],
    #             "discharging_samples": [],
    #             "cycles": [],
    #             "statistics": {}
    #         }

    #     self.view.reset_display(selected_duts)