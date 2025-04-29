import tkinter as tk
from tkinter import messagebox, simpledialog
from RonENG import MilitarySimulator
import random

class MilitarySimulatorApp:
    def __init__(self, root):
        self.simulator = MilitarySimulator()
        self.root = root
        self.root.title("Military Simulator")

        self.bg_color = "#2E2E2E"  
        self.button_bg = "#4E4E4E"  
        self.button_fg = "#FFFFFF"  
        self.text_color = "#FFFFFF"  
        self.accent_color = "#FF4500"  

        self.header_font = ("Arial Black", 16)
        self.button_font = ("Arial", 10, "bold")
        self.text_font = ("Arial", 10)

        self.header = tk.Label(root, text="Military Simulator", font=self.header_font, bg=self.bg_color, fg=self.text_color)
        self.header.pack(pady=10)

        self.main_content = tk.Frame(root, bg=self.bg_color)
        self.main_content.pack(fill=tk.BOTH, expand=True)

        self.left_panel = tk.Frame(self.main_content, width=200, bg=self.bg_color)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.create_menu_button("Manage Soldiers", self.show_soldier_menu)
        self.create_menu_button("Manage Teams", self.show_team_menu)
        self.create_menu_button("Manage Missions", self.show_mission_menu)
        self.create_menu_button("Simulation Controls", self.show_simulation_menu)
        self.create_menu_button("Reports", self.show_reports_menu)

        self.right_panel = tk.Frame(self.main_content, bg=self.bg_color)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.content_label = tk.Label(self.right_panel, text="Select an option from the left menu.", wraplength=400, bg=self.bg_color, fg=self.text_color, font=self.text_font)
        self.content_label.pack(pady=20)

    def create_menu_button(self, text, command):
        button = tk.Button(self.left_panel, text=text, command=command, width=20, bg=self.button_bg, fg=self.button_fg, font=self.button_font, relief=tk.RAISED, borderwidth=3)
        button.pack(pady=5)

    def clear_content(self):
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        self.content_label = tk.Label(self.right_panel, text="", wraplength=400, bg=self.bg_color, fg=self.text_color, font=self.text_font)
        self.content_label.pack(pady=20)

    def show_soldier_menu(self):
        self.clear_content()
        self.content_label.config(text="Soldier Management")

        self.create_action_button("Create New Soldier", self.create_soldier)
        self.create_action_button("View Soldier Details", self.view_soldier_details)
        self.create_action_button("Update Soldier Status", self.update_soldier_status)
        self.create_action_button("Add Equipment to Soldier", self.add_equipment_to_soldier)
        self.create_action_button("Update Soldier Health", self.update_soldier_health)
        self.create_action_button("List All Soldiers", self.list_all_soldiers)

    def show_team_menu(self):
        self.clear_content()
        self.content_label.config(text="Team Management")

        self.create_action_button("Create New Team", self.create_team)
        self.create_action_button("Add Soldier to Team", self.add_soldier_to_team)
        self.create_action_button("Set Team Commander", self.set_team_commander)
        self.create_action_button("View Team Status", self.view_team_status)
        self.create_action_button("Move Team", self.move_team)
        self.create_action_button("Generate Equipment Report", self.generate_equipment_report)
        self.create_action_button("Distribute Equipment", self.distribute_equipment)
        self.create_action_button("List All Teams", self.list_all_teams)

    def show_mission_menu(self):
        self.clear_content()
        self.content_label.config(text="Mission Management")

        self.create_action_button("Create New Mission", self.create_mission)
        self.create_action_button("Add Team to Mission", self.add_team_to_mission)
        self.create_action_button("Add Objective to Mission", self.add_objective_to_mission)
        self.create_action_button("Complete Objective", self.complete_objective)
        self.create_action_button("Change Mission Status", self.change_mission_status)
        self.create_action_button("View Mission Report", self.view_mission_report)
        self.create_action_button("Calculate Success Probability", self.calculate_success_probability)
        self.create_action_button("Set Mission Difficulty", self.set_mission_difficulty)
        self.create_action_button("List All Missions", self.list_all_missions)

    def show_simulation_menu(self):
        self.clear_content()
        self.content_label.config(text="Simulation Controls")

        self.create_action_button("Simulate Mission Progress", self.simulate_mission_progress)
        self.create_action_button("Auto-complete Mission", self.auto_complete_mission)
        self.create_action_button("Generate Casualty Event", self.generate_casualty_event)
        self.create_action_button("Generate Random Event", self.generate_random_event)

    def show_reports_menu(self):
        self.clear_content()
        self.content_label.config(text="Reports")

        self.create_action_button("Global Status Report", self.global_status_report)
        self.create_action_button("Team Skill Assessment", self.team_skill_assessment)
        self.create_action_button("Mission Success Probabilities", self.mission_success_probabilities)
        self.create_action_button("Recent Events Log", self.recent_events_log)
        self.create_action_button("Equipment Summary", self.equipment_summary)
        self.create_action_button("Personnel Status", self.personnel_status)

    def create_action_button(self, text, command):
        button = tk.Button(self.right_panel, text=text, command=command, width=30, bg=self.button_bg, fg=self.button_fg, font=self.button_font, relief=tk.RAISED, borderwidth=3)
        button.pack(pady=5)

    def create_soldier(self):
        name = simpledialog.askstring("Create Soldier", "Enter soldier name:")
        if name:
            rank = simpledialog.askstring("Create Soldier", "Enter rank (default: Private):") or "Private"
            status = simpledialog.askstring("Create Soldier", "Enter status (default: Active):") or "Active"
            soldier = self.simulator.create_soldier(name, status=status, rank=rank)
            self.content_label.config(text=f"Soldier created: {soldier}")

    def view_soldier_details(self):
        name = simpledialog.askstring("View Soldier Details", "Enter soldier name:")
        if name:
            soldier = self.simulator.find_soldier(name)
            if soldier:
                details = "\n".join([f"{key.capitalize()}: {value}" for key, value in soldier.report_status().items()])
                self.content_label.config(text=f"Soldier Details:\n{details}")
            else:
                self.content_label.config(text=f"Soldier '{name}' not found")

    def update_soldier_status(self):
        name = simpledialog.askstring("Update Soldier Status", "Enter soldier name:")
        if name:
            status = simpledialog.askstring("Update Soldier Status", "Enter new status (Active/Injured/Unavailable/OnLeave/MIA):")
            soldier = self.simulator.find_soldier(name)
            if soldier:
                if soldier.update_status(status):
                    self.content_label.config(text=f"Soldier {name} status updated to {status}")
                else:
                    self.content_label.config(text="Invalid status")
            else:
                self.content_label.config(text=f"Soldier '{name}' not found")

    def add_equipment_to_soldier(self):
        name = simpledialog.askstring("Add Equipment to Soldier", "Enter soldier name:")
        if name:
            item = simpledialog.askstring("Add Equipment to Soldier", "Enter equipment item:")
            quantity = simpledialog.askstring("Add Equipment to Soldier", "Enter quantity:")
            soldier = self.simulator.find_soldier(name)
            if soldier:
                try:
                    quantity = int(quantity)
                    soldier.add_equipment(item, quantity)
                    self.content_label.config(text=f"Added {quantity} {item} to {name}")
                except ValueError:
                    self.content_label.config(text="Invalid quantity")
            else:
                self.content_label.config(text=f"Soldier '{name}' not found")

    def update_soldier_health(self):
        name = simpledialog.askstring("Update Soldier Health", "Enter soldier name:")
        if name:
            health_change = simpledialog.askstring("Update Soldier Health", "Enter health change (positive to heal, negative for damage):")
            soldier = self.simulator.find_soldier(name)
            if soldier:
                try:
                    health_change = int(health_change)
                    new_health = soldier.update_health(health_change)
                    self.content_label.config(text=f"Soldier {name} health updated to {new_health}")
                except ValueError:
                    self.content_label.config(text="Invalid health change")
            else:
                self.content_label.config(text=f"Soldier '{name}' not found")

    def list_all_soldiers(self):
        soldiers = self.simulator.soldiers
        if not soldiers:
            self.content_label.config(text="No soldiers found")
        else:
            soldier_list = "\n".join([str(soldier) for soldier in soldiers])
            self.content_label.config(text=f"All Soldiers:\n{soldier_list}")

    def create_team(self):
        name = simpledialog.askstring("Create Team", "Enter team name:")
        if name:
            team = self.simulator.create_team(name)
            self.content_label.config(text=f"Team created: {team}")

    def add_soldier_to_team(self):
        team_name = simpledialog.askstring("Add Soldier to Team", "Enter team name:")
        if team_name:
            soldier_name = simpledialog.askstring("Add Soldier to Team", "Enter soldier name:")
            team = self.simulator.find_team(team_name)
            soldier = self.simulator.find_soldier(soldier_name)
            if team and soldier:
                team.add_member(soldier)
                self.content_label.config(text=f"Soldier {soldier_name} added to team {team_name}")
            else:
                self.content_label.config(text="Team or soldier not found")

    def set_team_commander(self):
        team_name = simpledialog.askstring("Set Team Commander", "Enter team name:")
        if team_name:
            soldier_name = simpledialog.askstring("Set Team Commander", "Enter soldier name:")
            team = self.simulator.find_team(team_name)
            soldier = self.simulator.find_soldier(soldier_name)
            if team and soldier:
                if team.set_commander(soldier):
                    self.content_label.config(text=f"{soldier_name} set as commander of team {team_name}")
                else:
                    self.content_label.config(text="Soldier not in team")
            else:
                self.content_label.config(text="Team or soldier not found")

    def view_team_status(self):
        team_name = simpledialog.askstring("View Team Status", "Enter team name:")
        if team_name:
            team = self.simulator.find_team(team_name)
            if team:
                self.content_label.config(text=team.team_status())
            else:
                self.content_label.config(text=f"Team '{team_name}' not found")

    def move_team(self):
        team_name = simpledialog.askstring("Move Team", "Enter team name:")
        if team_name:
            x = simpledialog.askstring("Move Team", "Enter X coordinate:")
            y = simpledialog.askstring("Move Team", "Enter Y coordinate:")
            team = self.simulator.find_team(team_name)
            if team:
                try:
                    x = int(x)
                    y = int(y)
                    team.move_team((x, y))
                    self.content_label.config(text=f"Team {team_name} moved to ({x}, {y})")
                except ValueError:
                    self.content_label.config(text="Invalid coordinates")
            else:
                self.content_label.config(text=f"Team '{team_name}' not found")

    def generate_equipment_report(self):
        team_name = simpledialog.askstring("Generate Equipment Report", "Enter team name:")
        if team_name:
            team = self.simulator.find_team(team_name)
            if team:
                self.content_label.config(text=team.equipment_report())
            else:
                self.content_label.config(text=f"Team '{team_name}' not found")

    def distribute_equipment(self):
        team_name = simpledialog.askstring("Distribute Equipment", "Enter team name:")
        if team_name:
            item = simpledialog.askstring("Distribute Equipment", "Enter equipment item:")
            quantity = simpledialog.askstring("Distribute Equipment", "Enter quantity:")
            team = self.simulator.find_team(team_name)
            if team:
                try:
                    quantity = int(quantity)
                    equipment_dict = {item: quantity}
                    team.distribute_equipment(equipment_dict)
                    self.content_label.config(text=f"Distributed {quantity} {item} to team {team_name}")
                except ValueError:
                    self.content_label.config(text="Invalid quantity")
            else:
                self.content_label.config(text=f"Team '{team_name}' not found")

    def list_all_teams(self):
        teams = self.simulator.teams
        if not teams:
            self.content_label.config(text="No teams found")
        else:
            team_list = "\n".join([str(team) for team in teams])
            self.content_label.config(text=f"All Teams:\n{team_list}")

    def create_mission(self):
        name = simpledialog.askstring("Create Mission", "Enter mission name:")
        if name:
            description = simpledialog.askstring("Create Mission", "Enter mission description:")
            x = simpledialog.askstring("Create Mission", "Enter X coordinate:")
            y = simpledialog.askstring("Create Mission", "Enter Y coordinate:")
            try:
                x = int(x)
                y = int(y)
                mission = self.simulator.create_mission(name, description, (x, y))
                self.content_label.config(text=f"Mission created: {mission}")
            except ValueError:
                self.content_label.config(text="Invalid coordinates")

    def add_team_to_mission(self):
        mission_name = simpledialog.askstring("Add Team to Mission", "Enter mission name:")
        if mission_name:
            team_name = simpledialog.askstring("Add Team to Mission", "Enter team name:")
            mission = self.simulator.find_mission(mission_name)
            team = self.simulator.find_team(team_name)
            if mission and team:
                mission.add_team(team)
                self.content_label.config(text=f"Team {team_name} added to mission {mission_name}")
            else:
                self.content_label.config(text="Mission or team not found")

    def add_objective_to_mission(self):
        mission_name = simpledialog.askstring("Add Objective to Mission", "Enter mission name:")
        if mission_name:
            objective = simpledialog.askstring("Add Objective to Mission", "Enter objective description:")
            mission = self.simulator.find_mission(mission_name)
            if mission:
                mission.add_objective(objective)
                self.content_label.config(text=f"Objective added to mission {mission_name}")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def complete_objective(self):
        mission_name = simpledialog.askstring("Complete Objective", "Enter mission name:")
        if mission_name:
            objective_index = simpledialog.askstring("Complete Objective", "Enter objective index (starting from 1):")
            mission = self.simulator.find_mission(mission_name)
            if mission:
                try:
                    index = int(objective_index) - 1
                    if mission.complete_objective(index):
                        self.content_label.config(text=f"Objective {index + 1} completed in mission {mission_name}")
                    else:
                        self.content_label.config(text="Invalid objective index")
                except ValueError:
                    self.content_label.config(text="Invalid index")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def change_mission_status(self):
        mission_name = simpledialog.askstring("Change Mission Status", "Enter mission name:")
        if mission_name:
            status = simpledialog.askstring("Change Mission Status", "Enter new status (Pending/Active/Completed/Failed/Aborted):")
            mission = self.simulator.find_mission(mission_name)
            if mission:
                if mission.update_status(status):
                    self.content_label.config(text=f"Mission {mission_name} status updated to {status}")
                else:
                    self.content_label.config(text="Invalid status")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def view_mission_report(self):
        mission_name = simpledialog.askstring("View Mission Report", "Enter mission name:")
        if mission_name:
            mission = self.simulator.find_mission(mission_name)
            if mission:
                self.content_label.config(text=mission.mission_report())
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def calculate_success_probability(self):
        mission_name = simpledialog.askstring("Calculate Success Probability", "Enter mission name:")
        if mission_name:
            mission = self.simulator.find_mission(mission_name)
            if mission:
                probability = mission.calculate_success_probability()
                self.content_label.config(text=f"Success probability for mission {mission_name}: {probability}%")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def set_mission_difficulty(self):
        mission_name = simpledialog.askstring("Set Mission Difficulty", "Enter mission name:")
        if mission_name:
            difficulty = simpledialog.askstring("Set Mission Difficulty", "Enter difficulty level (1-10):")
            mission = self.simulator.find_mission(mission_name)
            if mission:
                try:
                    difficulty = int(difficulty)
                    if mission.set_difficulty(difficulty):
                        self.content_label.config(text=f"Difficulty set to {difficulty} for mission {mission_name}")
                    else:
                        self.content_label.config(text="Invalid difficulty level")
                except ValueError:
                    self.content_label.config(text="Invalid difficulty")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def list_all_missions(self):
        missions = self.simulator.missions
        if not missions:
            self.content_label.config(text="No missions found")
        else:
            mission_list = "\n".join([str(mission) for mission in missions])
            self.content_label.config(text=f"All Missions:\n{mission_list}")

    def simulate_mission_progress(self):
        mission_name = simpledialog.askstring("Simulate Mission Progress", "Enter mission name:")
        if mission_name:
            mission = self.simulator.find_mission(mission_name)
            if mission:
                status = self.simulator.simulate_mission_progress(mission_name)
                self.content_label.config(text=f"Mission progress simulated. New status: {status}")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def auto_complete_mission(self):
        mission_name = simpledialog.askstring("Auto-complete Mission", "Enter mission name:")
        if mission_name:
            mission = self.simulator.find_mission(mission_name)
            if mission:
                if mission.status not in ["Completed", "Failed", "Aborted"]:
                    mission.update_status("Active")
                    for i in range(len(mission.objectives)):
                        mission.complete_objective(i)
                    mission.update_status("Completed")
                    self.content_label.config(text=f"Mission {mission_name} auto-completed")
                else:
                    self.content_label.config(text=f"Mission {mission_name} already finalized with status: {mission.status}")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def generate_casualty_event(self):
        team_name = simpledialog.askstring("Generate Casualty Event", "Enter team name:")
        if team_name:
            team = self.simulator.find_team(team_name)
            if team:
                active_members = [m for m in team.members if m.status == "Active"]
                if not active_members:
                    self.content_label.config(text="No active members in team")
                else:
                    victim = random.choice(active_members)
                    damage = random.randint(10, 50)
                    victim.update_health(-damage)
                    self.content_label.config(text=f"Casualty event: {victim.name} took {damage} damage")
            else:
                self.content_label.config(text=f"Team '{team_name}' not found")

    def generate_random_event(self):
        mission_name = simpledialog.askstring("Generate Random Event", "Enter mission name:")
        if mission_name:
            mission = self.simulator.find_mission(mission_name)
            if mission:
                events = [
                    "encountered unexpected resistance",
                    "discovered valuable intelligence",
                    "experienced equipment malfunction",
                    "weather conditions deteriorated",
                    "found alternate route",
                    "communications disrupted",
                    "supply drop received",
                    "encountered friendly forces",
                    "detected enemy patrol",
                    "secured key position"
                ]
                event = random.choice(events)
                mission.log_event(f"Random event: {event}")
                self.content_label.config(text=f"Random event generated for mission {mission_name}: {event}")
            else:
                self.content_label.config(text=f"Mission '{mission_name}' not found")

    def global_status_report(self):
        self.content_label.config(text=self.simulator.global_status_report())

    def team_skill_assessment(self):
        teams = self.simulator.teams
        if not teams:
            self.content_label.config(text="No teams found")
        else:
            report = "\n".join([team.team_skill_report() for team in teams])
            self.content_label.config(text=f"Team Skill Assessment:\n{report}")

    def mission_success_probabilities(self):
        missions = self.simulator.missions
        if not missions:
            self.content_label.config(text="No missions found")
        else:
            report = "\n".join([f"Mission: {mission.name}\nSuccess Probability: {mission.calculate_success_probability()}%" for mission in missions])
            self.content_label.config(text=f"Mission Success Probabilities:\n{report}")

    def recent_events_log(self):
        logs = self.simulator.events_log
        if not logs:
            self.content_label.config(text="No recent events")
        else:
            logs_to_show = min(20, len(logs))
            self.content_label.config(text=f"Recent Events Log:\n" + "\n".join(logs[-logs_to_show:]))

    def equipment_summary(self):
        all_equipment = {}
        for soldier in self.simulator.soldiers:
            for item, qty in soldier.equipment.items():
                if item in all_equipment:
                    all_equipment[item] += qty
                else:
                    all_equipment[item] = qty
        if not all_equipment:
            self.content_label.config(text="No equipment found")
        else:
            report = "\n".join([f"- {item}: {qty} units" for item, qty in all_equipment.items()])
            self.content_label.config(text=f"Equipment Summary:\n{report}")

    def personnel_status(self):
        status_groups = {}
        for soldier in self.simulator.soldiers:
            if soldier.status not in status_groups:
                status_groups[soldier.status] = []
            status_groups[soldier.status].append(soldier)
        if not status_groups:
            self.content_label.config(text="No personnel found")
        else:
            report = "\n".join([f"\n{status} Personnel ({len(soldiers)}):\n" + "\n".join([f"- {soldier.rank} {soldier.name}, Health: {soldier.health}%" for soldier in soldiers]) for status, soldiers in status_groups.items()])
            self.content_label.config(text=f"Personnel Status:\n{report}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MilitarySimulatorApp(root)
    root.mainloop()