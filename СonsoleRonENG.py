import time
import os
import random
from datetime import datetime

class Soldier:
    RANKS = ["Private", "Corporal", "Sergeant", "Lieutenant", "Captain", "Major"]
    STATUS_TYPES = ["Active", "Injured", "Unavailable", "OnLeave", "MIA"]
    
    def __init__(self, name, status, location, rank="Private", health=100, equipment=None):
        self.name = name
        self.status = status if status in self.STATUS_TYPES else "Active"
        self.location = location  # (x, y) coordinates
        self.rank = rank
        self.health = health
        self.equipment = equipment or {}
        self.mission = None
        self.messages_received = []
        self.experience = 0
        self.skills = {"combat": 1, "medical": 1, "recon": 1, "leadership": 1}
        self.history = []
        self.log_event(f"Soldier created with rank {rank}")
    
    def update_status(self, new_status):
        if new_status not in self.STATUS_TYPES:
            return False
            
        old_status = self.status
        self.status = new_status
        self.log_event(f"Status updated from {old_status} to {self.status}")
        return True
    
    def update_location(self, new_location):
        distance = self._calculate_distance(self.location, new_location)
        self.location = new_location
        self.log_event(f"Location updated to {self.location} (moved {distance:.2f} units)")
        return True
    
    def send_message(self, message):
        msg = f"{self.rank} {self.name} sends: {message}"
        self.log_event(f"Sent message: {message}")
        return msg
    
    def receive_message(self, sender, message):
        self.messages_received.append((sender, message, datetime.now()))
        self.log_event(f"Received message from {sender}")
    
    def assign_mission(self, mission):
        self.mission = mission
        self.log_event(f"Assigned to mission: {mission}")
    
    def update_health(self, amount):
        old_health = self.health
        self.health += amount
        
        if self.health > 100:
            self.health = 100
        elif self.health <= 0:
            self.health = 0
            self.status = "Injured"
            self.log_event("Injured and needs medical attention!")
        
        self.log_event(f"Health changed from {old_health} to {self.health}")
        return self.health
    
    def add_equipment(self, item, quantity=1):
        if item in self.equipment:
            self.equipment[item] += quantity
        else:
            self.equipment[item] = quantity
        self.log_event(f"Received {quantity} {item}")
    
    def use_equipment(self, item, quantity=1):
        if item in self.equipment and self.equipment[item] >= quantity:
            self.equipment[item] -= quantity
            self.log_event(f"Used {quantity} {item}")
            if self.equipment[item] == 0:
                del self.equipment[item]
            return True
        else:
            self.log_event(f"Not enough {item}")
            return False
    
    def report_status(self):
        return {
            "name": self.name,
            "rank": self.rank,
            "status": self.status,
            "location": self.location,
            "health": self.health,
            "equipment": self.equipment,
            "mission": self.mission,
            "experience": self.experience,
            "skills": self.skills
        }
    
    def gain_experience(self, amount):
        self.experience += amount
        self.log_event(f"Gained {amount} experience points")
        
        # Check if rank promotion is possible
        current_rank_index = self.RANKS.index(self.rank) if self.rank in self.RANKS else 0
        if self.experience >= 100 * (current_rank_index + 1) and current_rank_index < len(self.RANKS) - 1:
            self.rank = self.RANKS[current_rank_index + 1]
            self.log_event(f"Promoted to {self.rank}")
    
    def improve_skill(self, skill_name, amount=1):
        if skill_name in self.skills:
            self.skills[skill_name] += amount
            self.log_event(f"Improved {skill_name} skill by {amount}")
            return True
        return False
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: {self.rank} {self.name} - {description}"
        self.history.append(event)
        return event
    
    def _calculate_distance(self, point1, point2):
        return ((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2) ** 0.5
    
    def __str__(self):
        return f"{self.rank} {self.name} ({self.status}, Health: {self.health}%)"


class Team:
    def __init__(self, name, commander=None):
        self.name = name
        self.members = []
        self.commander = commander
        self.mission_log = []
        self.created_date = datetime.now()
        self.team_chat = []
        self.equipment_inventory = {}
        self.location = (0, 0)
        self.status = "Standby"
    
    def add_member(self, soldier):
        self.members.append(soldier)
        self.log_event(f"{soldier.rank} {soldier.name} added to team")
        return True
    
    def remove_member(self, soldier):
        if soldier in self.members:
            self.members.remove(soldier)
            self.log_event(f"{soldier.rank} {soldier.name} removed from team")
            return True
        return False
    
    def set_commander(self, soldier):
        if soldier in self.members:
            self.commander = soldier
            self.log_event(f"{soldier.rank} {soldier.name} is now commander")
            return True
        else:
            self.log_event(f"{soldier.rank} {soldier.name} is not in team")
            return False
    
    def team_status(self):
        active_count = sum(1 for member in self.members if member.status == "Active")
        injured_count = sum(1 for member in self.members if member.status == "Injured")
        
        status_report = f"\nTeam {self.name} Status Report:\n"
        status_report += f"Total members: {len(self.members)}, Active: {active_count}, Injured: {injured_count}\n"
        
        if self.commander:
            status_report += f"Commander: {self.commander.rank} {self.commander.name}\n"
        
        status_report += f"Current location: {self.location}\n"
        status_report += f"Current status: {self.status}\n\n"
        
        status_report += "Members:\n"
        for member in self.members:
            status_report += f"{member.rank} {member.name}: {member.status} at {member.location}, Health: {member.health}%\n"
        
        self.log_event("Team status report generated")
        return status_report
    
    def broadcast_message(self, message, sender="HQ"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        broadcast = f"{timestamp} - {sender}: {message}"
        self.team_chat.append(broadcast)
        
        for member in self.members:
            member.receive_message(sender, message)
        
        self.log_event(f"Message broadcast from {sender}: {message}")
        return True
    
    def direct_message(self, sender, recipient_name, message):
        for member in self.members:
            if member.name == recipient_name:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dm = f"{timestamp} - {sender} to {recipient_name}: {message}"
                self.team_chat.append(dm)
                
                member.receive_message(sender, message)
                self.log_event(f"Direct message from {sender} to {recipient_name}")
                return True
                
        self.log_event(f"Recipient {recipient_name} not found")
        return False
    
    def assign_team_mission(self, mission_description):
        mission_id = len(self.mission_log) + 1
        mission = f"Mission #{mission_id}: {mission_description}"
        
        for member in self.members:
            if member.status == "Active":
                member.assign_mission(mission)
        
        self.mission_log.append(mission)
        self.status = "On Mission"
        self.log_event(f"Team assigned to {mission}")
        return mission_id
    
    def move_team(self, new_location, formation_spacing=5):
        if not self.members:
            return False
        
        self.log_event(f"Moving team to {new_location}")
        
        # Create formation pattern centered around the target location
        positions = []
        for i, member in enumerate(self.members):
            if member.status == "Active":
                # Simple formation pattern
                if i == 0:  # Commander or first soldier at center
                    pos = new_location
                elif i % 2 == 1:  # Positions to right
                    offset = ((i + 1) // 2) * formation_spacing
                    pos = (new_location[0] + offset, new_location[1])
                else:  # Positions to left
                    offset = (i // 2) * formation_spacing
                    pos = (new_location[0] - offset, new_location[1])
                
                positions.append((member, pos))
        
        # Execute movement
        for member, pos in positions:
            member.update_location(pos)
        
        self.location = new_location
        return True
    
    def equipment_report(self):
        report = {}
        for member in self.members:
            for item, quantity in member.equipment.items():
                if item in report:
                    report[item] += quantity
                else:
                    report[item] = quantity
        
        self.equipment_inventory = report
        self.log_event("Equipment report generated")
        
        report_str = f"\nTeam {self.name} Equipment Report:\n"
        for item, quantity in report.items():
            report_str += f"- {item}: {quantity}\n"
        
        return report_str
    
    def distribute_equipment(self, equipment_dict):
        """Distribute equipment evenly among active team members"""
        active_members = [m for m in self.members if m.status == "Active"]
        if not active_members:
            self.log_event("No active members to distribute equipment to")
            return False
            
        for item, quantity in equipment_dict.items():
            per_person = quantity // len(active_members)
            remainder = quantity % len(active_members)
            
            if per_person > 0:
                for member in active_members:
                    member.add_equipment(item, per_person)
                    
            # Distribute remainder
            for i in range(remainder):
                active_members[i].add_equipment(item, 1)
                
        self.log_event(f"Equipment distributed among {len(active_members)} active members")
        return True
    
    def team_skill_report(self):
        """Generate a report of team's combined skills"""
        skills = {"combat": 0, "medical": 0, "recon": 0, "leadership": 0}
        
        for member in self.members:
            for skill, value in member.skills.items():
                if skill in skills:
                    skills[skill] += value
        
        report_str = f"\nTeam {self.name} Skill Report:\n"
        for skill, value in skills.items():
            avg = value / len(self.members) if self.members else 0
            report_str += f"- {skill.capitalize()}: Total {value}, Avg {avg:.1f}\n"
            
        self.log_event("Team skill report generated")
        return report_str
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: Team {self.name} - {description}"
        self.mission_log.append(event)
        return event
    
    def __str__(self):
        return f"Team {self.name} ({len(self.members)} members, Commander: {self.commander.name if self.commander else 'None'})"


class Mission:
    STATUS_TYPES = ["Pending", "Active", "Completed", "Failed", "Aborted"]
    
    def __init__(self, name, description, location, teams=None):
        self.name = name
        self.description = description
        self.location = location
        self.teams = teams or []
        self.status = "Pending"
        self.objectives = []
        self.events = []
        self.start_time = None
        self.end_time = None
        self.difficulty = 1  # 1-10 scale
        self.success_rate = 0
        self.rewards = {"experience": 10}
        
        self.log_event(f"Mission created: {name}")
    
    def add_team(self, team):
        self.teams.append(team)
        self.log_event(f"Team {team.name} added to mission")
        return True
    
    def add_objective(self, objective, completed=False):
        self.objectives.append({"description": objective, "completed": completed, "added": datetime.now()})
        self.log_event(f"Objective added: {objective}")
        return True
    
    def complete_objective(self, index):
        if 0 <= index < len(self.objectives):
            self.objectives[index]["completed"] = True
            self.objectives[index]["completed_time"] = datetime.now()
            self.log_event(f"Objective completed: {self.objectives[index]['description']}")
            
            # Check if all objectives completed
            if all(obj["completed"] for obj in self.objectives):
                self.status = "Completed"
                self.end_time = datetime.now()
                self.success_rate = 100
                self.log_event("All objectives completed")
                
                # Award experience to team members
                for team in self.teams:
                    for member in team.members:
                        member.gain_experience(self.rewards["experience"])
                
            return True
        return False
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: {description}"
        self.events.append(event)
        return event
    
    def update_status(self, new_status):
        if new_status not in self.STATUS_TYPES:
            return False
            
        old_status = self.status
        self.status = new_status
        
        if new_status == "Active" and not self.start_time:
            self.start_time = datetime.now()
        elif new_status in ["Completed", "Failed", "Aborted"] and not self.end_time:
            self.end_time = datetime.now()
            
        self.log_event(f"Status updated from {old_status} to {self.status}")
        return True
    
    def set_difficulty(self, level):
        """Set mission difficulty on 1-10 scale"""
        if 1 <= level <= 10:
            self.difficulty = level
            self.rewards["experience"] = level * 10  # Higher difficulty, higher rewards
            self.log_event(f"Difficulty set to {level}")
            return True
        return False
    
    def add_reward(self, reward_type, value):
        self.rewards[reward_type] = value
        self.log_event(f"Added reward: {reward_type} = {value}")
        return True
    
    def mission_report(self):
        completed = sum(1 for obj in self.objectives if obj["completed"])
        
        report = f"\nMission Report: {self.name}\n"
        report += f"Status: {self.status}\n"
        report += f"Location: {self.location}\n"
        report += f"Description: {self.description}\n"
        report += f"Difficulty: {self.difficulty}/10\n"
        
        if self.start_time:
            report += f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if self.end_time:
            report += f"End time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            if self.start_time:
                duration = self.end_time - self.start_time
                report += f"Duration: {duration}\n"
        
        report += f"Objectives: {completed}/{len(self.objectives)} completed\n"
        
        for i, obj in enumerate(self.objectives):
            status = "✓" if obj["completed"] else "✗"
            report += f"  {status} {i+1}. {obj['description']}\n"
        
        report += "\nTeams assigned:\n"
        for team in self.teams:
            report += f"- {team.name} ({len(team.members)} members)\n"
        
        if self.events:
            report += "\nRecent events:\n"
            for event in self.events[-5:]:
                report += f"  - {event}\n"
        
        self.log_event("Mission report generated")
        return report
    
    def calculate_success_probability(self):
        """Calculate probability of mission success based on team composition"""
        if not self.teams or not any(team.members for team in self.teams):
            return 0
            
        total_members = sum(len(team.members) for team in self.teams)
        active_members = sum(sum(1 for m in team.members if m.status == "Active") for team in self.teams)
        
        if active_members == 0:
            return 0
            
        active_ratio = active_members / total_members
        
        # Calculate average relevant skills across all teams
        combat = medical = recon = leadership = 0
        for team in self.teams:
            for member in team.members:
                if member.status == "Active":
                    combat += member.skills["combat"]
                    medical += member.skills["medical"]
                    recon += member.skills["recon"]
                    leadership += member.skills["leadership"]
        
        # Average skill level (1-10 scale)
        avg_skill = (combat + medical + recon + leadership) / (active_members * 4) if active_members > 0 else 0
        
        # Success probability formula: normalized skill vs difficulty, adjusted by active ratio
        probability = (avg_skill / 10) * (1 / self.difficulty) * active_ratio * 100
        probability = min(100, max(0, probability))
        
        self.success_rate = round(probability, 1)
        self.log_event(f"Success probability calculated: {self.success_rate}%")
        return self.success_rate
    
    def __str__(self):
        return f"Mission: {self.name} ({self.status})"


class MilitarySimulator:
    def __init__(self):
        self.soldiers = []
        self.teams = []
        self.missions = []
        self.events_log = []
        self.equipment_database = {
            "Rifle": {"weight": 4.5, "effectiveness": 7},
            "Pistol": {"weight": 1.0, "effectiveness": 4},
            "Medkit": {"weight": 2.0, "effectiveness": 8},
            "Radio": {"weight": 1.5, "effectiveness": 6},
            "Binoculars": {"weight": 1.0, "effectiveness": 5},
            "Ammo": {"weight": 0.5, "effectiveness": 6},
            "Grenade": {"weight": 0.7, "effectiveness": 8},
            "Rations": {"weight": 1.0, "effectiveness": 3},
            "Water": {"weight": 1.5, "effectiveness": 4},
            "Night Vision": {"weight": 1.2, "effectiveness": 7}
        }
        self.log_event("Military Simulator initialized")
    
    def create_soldier(self, name, status="Active", location=(0, 0), rank="Private"):
        soldier = Soldier(name, status, location, rank)
        self.soldiers.append(soldier)
        self.log_event(f"Soldier created: {name}")
        return soldier
    
    def create_team(self, name):
        team = Team(name)
        self.teams.append(team)
        self.log_event(f"Team created: {name}")
        return team
    
    def create_mission(self, name, description, location):
        mission = Mission(name, description, location)
        self.missions.append(mission)
        self.log_event(f"Mission created: {name}")
        return mission
    
    def assign_soldier_to_team(self, soldier_name, team_name):
        soldier = self.find_soldier(soldier_name)
        team = self.find_team(team_name)
        
        if soldier and team:
            team.add_member(soldier)
            self.log_event(f"{soldier.name} assigned to team {team.name}")
            return True
        return False
    
    def assign_team_to_mission(self, team_name, mission_name):
        team = self.find_team(team_name)
        mission = self.find_mission(mission_name)
        
        if team and mission:
            mission.add_team(team)
            team.assign_team_mission(mission.name)
            self.log_event(f"Team {team.name} assigned to mission {mission.name}")
            return True
        return False
    
    def find_soldier(self, name):
        for soldier in self.soldiers:
            if soldier.name.lower() == name.lower():
                return soldier
        return None
    
    def find_team(self, name):
        for team in self.teams:
            if team.name.lower() == name.lower():
                return team
        return None
    
    def find_mission(self, name):
        for mission in self.missions:
            if mission.name.lower() == name.lower():
                return mission
        return None
    
    def log_event(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp}: {description}"
        self.events_log.append(event)
        return event
    
    def global_status_report(self):
        report = "\n===== GLOBAL STATUS REPORT =====\n"
        
        report += f"Total personnel: {len(self.soldiers)}\n"
        report += f"Active teams: {len(self.teams)}\n"
        report += f"Missions: {len(self.missions)}\n\n"
        
        status_counts = {}
        for soldier in self.soldiers:
            if soldier.status in status_counts:
                status_counts[soldier.status] += 1
            else:
                status_counts[soldier.status] = 1
                
        report += "Personnel status:\n"
        for status, count in status_counts.items():
            report += f"- {status}: {count}\n"
        
        mission_status = {}
        for mission in self.missions:
            if mission.status in mission_status:
                mission_status[mission.status] += 1
            else:
                mission_status[mission.status] = 1
                
        report += "\nMission status:\n"
        for status, count in mission_status.items():
            report += f"- {status}: {count}\n"
        
        return report
    
    def distribute_equipment(self, team_name, equipment_dict):
        team = self.find_team(team_name)
        if team:
            return team.distribute_equipment(equipment_dict)
        return False
    
    def simulate_mission_progress(self, mission_name, success_chance=None):
        """Simulate mission progress automatically"""
        mission = self.find_mission(mission_name)
        if not mission:
            return False
            
        if mission.status not in ["Pending", "Active"]:
            return False
            
        # Start mission if pending
        if mission.status == "Pending":
            mission.update_status("Active")
            
        # Calculate success chance if not provided
        if success_chance is None:
            success_chance = mission.calculate_success_probability()
            
        # Process each objective
        for i, objective in enumerate(mission.objectives):
            if not objective["completed"]:
                # Random chance to complete objective based on success probability
                if random.random() * 100 < success_chance:
                    mission.complete_objective(i)
                    
                    # Random events during mission
                    if random.random() < 0.3:  # 30% chance of random event
                        events = [
                            "encountered light resistance",
                            "found valuable intelligence",
                            "had to find alternate route",
                            "equipment malfunction occurred",
                            "weather conditions worsened"
                        ]
                        mission.log_event(f"Random event: {random.choice(events)}")
                    
                    # Random injuries
                    if random.random() < 0.2:  # 20% chance of injury
                        for team in mission.teams:
                            for member in team.members:
                                if member.status == "Active" and random.random() < 0.1:
                                    damage = random.randint(5, 25)
                                    member.update_health(-damage)
                                    mission.log_event(f"{member.name} took {damage} damage")
                else:
                    # Objective failed
                    mission.log_event(f"Failed to complete objective: {objective['description']}")
                    if random.random() < 0.3:  # 30% chance of mission failure on objective failure
                        mission.update_status("Failed")
                        return mission.status
                        
                break  # Process one objective at a time
                
        return mission.status
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display the main menu"""
        self.clear_screen()
        print("\n===== MILITARY SIMULATOR =====")
        print("1. Manage Soldiers")
        print("2. Manage Teams")
        print("3. Manage Missions")
        print("4. Simulation Controls")
        print("5. Reports")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        return choice
    
    def soldier_menu(self):
        """Display soldier management menu"""
        self.clear_screen()
        print("\n===== SOLDIER MANAGEMENT =====")
        print("1. Create New Soldier")
        print("2. View Soldier Details")
        print("3. Update Soldier Status")
        print("4. Add Equipment to Soldier")
        print("5. Update Soldier Health")
        print("6. List All Soldiers")
        print("7. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            name = input("Enter soldier name: ")
            rank = input("Enter soldier rank (default: Private): ") or "Private"
            status = input("Enter status (Active/Injured/Unavailable, default: Active): ") or "Active"
            
            soldier = self.create_soldier(name, status=status, rank=rank)
            print(f"Soldier created: {soldier}")
            
        elif choice == "2":
            name = input("Enter soldier name: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print("\n===== SOLDIER DETAILS =====")
                for key, value in soldier.report_status().items():
                    print(f"{key.capitalize()}: {value}")
                    
                print("\nRecent history:")
                for event in soldier.history[-5:]:
                    print(f"- {event}")
            else:
                print(f"Soldier '{name}' not found")
                
        elif choice == "3":
            name = input("Enter soldier name: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print(f"Current status: {soldier.status}")
                status = input("Enter new status (Active/Injured/Unavailable/OnLeave/MIA): ")
                if soldier.update_status(status):
                    print(f"Status updated to {status}")
                else:
                    print("Invalid status")
            else:
                print(f"Soldier '{name}' not found")
                
        elif choice == "4":
            name = input("Enter soldier name: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print("Available equipment:")
                for item in self.equipment_database:
                    print(f"- {item}")
                    
                item = input("Enter equipment to add: ")
                if item in self.equipment_database:
                    try:
                        quantity = int(input("Enter quantity: "))
                        soldier.add_equipment(item, quantity)
                        print(f"Added {quantity} {item} to {soldier.name}")
                    except ValueError:
                        print("Invalid quantity")
                else:
                    print(f"Equipment '{item}' not found in database")
            else:
                print(f"Soldier '{name}' not found")
                
        elif choice == "5":
            name = input("Enter soldier name: ")
            soldier = self.find_soldier(name)
            
            if soldier:
                print(f"Current health: {soldier.health}")
                try:
                    amount = int(input("Enter health change (positive to heal, negative for damage): "))
                    new_health = soldier.update_health(amount)
                    print(f"Health updated to {new_health}")
                except ValueError:
                    print("Invalid input")
            else:
                print(f"Soldier '{name}' not found")
                
        elif choice == "6":
            if not self.soldiers:
                print("No soldiers found")
            else:
                print("\n===== ALL SOLDIERS =====")
                for i, soldier in enumerate(self.soldiers, 1):
                    print(f"{i}. {soldier}")
                    
        input("\nPress Enter to continue...")
        
    def team_menu(self):
        """Display team management menu"""
        self.clear_screen()
        print("\n===== TEAM MANAGEMENT =====")
        print("1. Create New Team")
        print("2. Add Soldier to Team")
        print("3. Set Team Commander")
        print("4. View Team Status")
        print("5. Move Team")
        print("6. Generate Equipment Report")
        print("7. Distribute Equipment")
        print("8. List All Teams")
        print("9. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == "1":
            name = input("Enter team name: ")
            team = self.create_team(name)
            print(f"Team created: {team}")
            
        elif choice == "2":
            team_name = input("Enter team name: ")
            team = self.find_team(team_name)
            
            if team:
                soldier_name = input("Enter soldier name to add: ")
                soldier = self.find_soldier(soldier_name)
                
                if soldier:
                    team.add_member(soldier)
                    print(f"{soldier.name} added to team {team_name}")
                else:
                    print(f"Soldier '{soldier_name}' not found")
            else:
                print(f"Team '{team_name}' not found")
                
        elif choice == "3":
            team_name = input("Enter team name: ")
            team = self.find_team(team_name)
            
            if team:
                print("Current team members:")
                for i, member in enumerate(team.members, 1):
                    print(f"{i}. {member}")
                    
                commander_name = input("Enter the name of the soldier to set as commander: ")
                commander = self.find_soldier(commander_name)
                
                if commander and commander in team.members:
                    team.set_commander(commander)
                    print(f"{commander.name} set as commander of team {team_name}")
                else:
                    print(f"Soldier '{commander_name}' not found or not in team")
            else:
                print(f"Team '{team_name}' not found")
                
        elif choice == "4":
            team_name = input("Enter team name: ")
            team = self.find_team(team_name)
            
            if team:
                print(team.team_status())
            else:
                print(f"Team '{team_name}' not found")
                
        elif choice == "5":
            team_name = input("Enter team name: ")
            team = self.find_team(team_name)
            
            if team:
                try:
                    x = int(input("Enter x-coordinate: "))
                    y = int(input("Enter y-coordinate: "))
                    
                    spacing = int(input("Enter formation spacing (default: 5): ") or "5")
                    
                    team.move_team((x, y), formation_spacing=spacing)
                    print(f"Team {team_name} moved to ({x}, {y})")
                except ValueError:
                    print("Invalid coordinate format")
            else:
                print(f"Team '{team_name}' not found")
                
        elif choice == "6":
            team_name = input("Enter team name: ")
            team = self.find_team(team_name)
            
            if team:
                print(team.equipment_report())
            else:
                print(f"Team '{team_name}' not found")
                
        elif choice == "7":
            team_name = input("Enter team name: ")
            team = self.find_team(team_name)
            
            if team:
                print("Available equipment:")
                for item in self.equipment_database:
                    print(f"- {item}")
                    
                equipment = {}
                while True:
                    item = input("Enter equipment to distribute (or 'done' to finish): ")
                    if item.lower() == 'done':
                        break
                    
                    if item in self.equipment_database:
                        try:
                            quantity = int(input("Enter quantity: "))
                            equipment[item] = quantity
                        except ValueError:
                            print("Invalid quantity")
                    else:
                        print(f"Equipment '{item}' not found in database")
                
                if equipment:
                    team.distribute_equipment(equipment)
                    print(f"Equipment distributed to team {team_name}")
            else:
                print(f"Team '{team_name}' not found")
                
        elif choice == "8":
            if not self.teams:
                print("No teams found")
            else:
                print("\n===== ALL TEAMS =====")
                for i, team in enumerate(self.teams, 1):
                    commander_name = team.commander.name if team.commander else "None"
                    print(f"{i}. {team.name} - Members: {len(team.members)}, Commander: {commander_name}")
                    
        input("\nPress Enter to continue...")
        
    def mission_menu(self):
        """Display mission management menu"""
        self.clear_screen()
        print("\n===== MISSION MANAGEMENT =====")
        print("1. Create New Mission")
        print("2. Add Team to Mission")
        print("3. Add Objective to Mission")
        print("4. Complete Objective")
        print("5. Change Mission Status")
        print("6. View Mission Report")
        print("7. Calculate Success Probability")
        print("8. Set Mission Difficulty")
        print("9. List All Missions")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice (0-9): ")
        
        if choice == "1":
            name = input("Enter mission name: ")
            description = input("Enter mission description: ")
            
            try:
                x = int(input("Enter x-coordinate: "))
                y = int(input("Enter y-coordinate: "))
                location = (x, y)
                
                mission = self.create_mission(name, description, location)
                
                difficulty = input("Enter mission difficulty (1-10, default: 1): ") or "1"
                try:
                    mission.set_difficulty(int(difficulty))
                except ValueError:
                    print("Invalid difficulty, using default")
                    
                print(f"Mission created: {mission}")
            except ValueError:
                print("Invalid coordinate format")
                
        elif choice == "2":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                team_name = input("Enter team name to add: ")
                team = self.find_team(team_name)
                
                if team:
                    mission.add_team(team)
                    team.assign_team_mission(mission.name)
                    print(f"Team {team_name} added to mission {mission_name}")
                else:
                    print(f"Team '{team_name}' not found")
            else:
                print(f"Mission '{mission_name}' not found")
                
        elif choice == "3":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                objective = input("Enter objective description: ")
                mission.add_objective(objective)
                print(f"Objective added to mission {mission_name}")
            else:
                print(f"Mission '{mission_name}' not found")
                
        elif choice == "4":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                print("Current objectives:")
                for i, obj in enumerate(mission.objectives):
                    status = "✓" if obj["completed"] else "✗"
                    print(f"{i+1}. {status} {obj['description']}")
                    
                try:
                    index = int(input("Enter objective number to complete: ")) - 1
                    if mission.complete_objective(index):
                        print("Objective completed")
                    else:
                        print("Invalid objective number")
                except ValueError:
                    print("Invalid input")
            else:
                print(f"Mission '{mission_name}' not found")
              
        elif choice == "5":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                print(f"Current status: {mission.status}")
                print("Available statuses: Pending, Active, Completed, Failed, Aborted")
                
                status = input("Enter new status: ")
                if mission.update_status(status):
                    print(f"Status updated to {status}")
                else:
                    print("Invalid status")
            else:
                print(f"Mission '{mission_name}' not found")
              
        elif choice == "6":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                print(mission.mission_report())
            else:
                print(f"Mission '{mission_name}' not found")
              
        elif choice == "7":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                probability = mission.calculate_success_probability()
                print(f"Mission success probability: {probability}%")
            else:
                print(f"Mission '{mission_name}' not found")
              
        elif choice == "8":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                try:
                    difficulty = int(input("Enter difficulty level (1-10): "))
                    if mission.set_difficulty(difficulty):
                        print(f"Difficulty set to {difficulty}")
                    else:
                        print("Invalid difficulty level")
                except ValueError:
                    print("Invalid input")
            else:
                print(f"Mission '{mission_name}' not found")
              
        elif choice == "9":
            if not self.missions:
                print("No missions found")
            else:
                print("\n===== ALL MISSIONS =====")
                for i, mission in enumerate(self.missions, 1):
                    completed = sum(1 for obj in mission.objectives if obj["completed"])
                    total = len(mission.objectives)
                    print(f"{i}. {mission.name} - Status: {mission.status}, Objectives: {completed}/{total}, Teams: {len(mission.teams)}")
                    
        input("\nPress Enter to continue...")
    
    def simulation_menu(self):
        """Display simulation controls menu"""
        self.clear_screen()
        print("\n===== SIMULATION CONTROLS =====")
        print("1. Simulate Mission Progress")
        print("2. Auto-complete Mission")
        print("3. Generate Casualty Event")
        print("4. Generate Random Event")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                status = self.simulate_mission_progress(mission_name)
                print(f"Mission progress simulated. New status: {status}")
            else:
                print(f"Mission '{mission_name}' not found")
              
        elif choice == "2":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
            if mission:
                if mission.status not in ["Completed", "Failed", "Aborted"]:
                    mission.update_status("Active")
                    
                    print(f"Auto-completing mission {mission_name}...")
                    for i in range(len(mission.objectives)):
                        if not mission.objectives[i]["completed"]:
                            mission.complete_objective(i)
                            time.sleep(0.5)  # Small delay for effect
                    
                    mission.update_status("Completed")
                    print(f"Mission {mission_name} auto-completed")
                else:
                    print(f"Mission {mission_name} already finalized with status: {mission.status}")
            else:
                print(f"Mission '{mission_name}' not found")
              
        elif choice == "3":
            team_name = input("Enter team name: ")
            team = self.find_team(team_name)
            
            if team:
                active_members = [m for m in team.members if m.status == "Active"]
                if not active_members:
                    print("No active members in team")
                else:
                    victim = random.choice(active_members)
                    damage = random.randint(10, 50)
                    
                    print(f"Casualty event generated for {victim.name}")
                    victim.update_health(-damage)
                    
                    team.log_event(f"Casualty event: {victim.name} took {damage} damage")
                    print(f"{victim.name}'s health reduced to {victim.health}")
                    
                    if victim.status == "Injured":
                        print(f"{victim.name} is now injured and requires medical attention!")
            else:
                print(f"Team '{team_name}' not found")
              
        elif choice == "4":
            mission_name = input("Enter mission name: ")
            mission = self.find_mission(mission_name)
            
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
                print(f"Random event generated for mission {mission_name}: {event}")
            else:
                print(f"Mission '{mission_name}' not found")
              
        input("\nPress Enter to continue...")
    
    def reports_menu(self):
        """Display reports menu"""
        self.clear_screen()
        print("\n===== REPORTS =====")
        print("1. Global Status Report")
        print("2. Team Skill Assessment")
        print("3. Mission Success Probabilities")
        print("4. Recent Events Log")
        print("5. Equipment Summary")
        print("6. Personnel Status")
        print("7. Back to Main Menu")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            print(self.global_status_report())
              
        elif choice == "2":
            print("\n===== TEAM SKILL ASSESSMENT =====")
            if not self.teams:
                print("No teams found")
            else:
                for team in self.teams:
                    print(team.team_skill_report())
              
        elif choice == "3":
            print("\n===== MISSION SUCCESS PROBABILITIES =====")
            if not self.missions:
                print("No missions found")
            else:
                for mission in self.missions:
                    probability = mission.calculate_success_probability()
                    print(f"Mission: {mission.name}")
                    print(f"Status: {mission.status}")
                    print(f"Difficulty: {mission.difficulty}/10")
                    print(f"Success probability: {probability}%")
                    
                    # Show why based on team composition
                    print("Factors affecting probability:")
                    
                    # Team count
                    team_count = len(mission.teams)
                    print(f"- Teams assigned: {team_count}")
                    
                    # Personnel count
                    total_personnel = sum(len(team.members) for team in mission.teams)
                    active_personnel = sum(sum(1 for m in team.members if m.status == "Active") for team in mission.teams)
                    print(f"- Personnel: {active_personnel} active out of {total_personnel} total")
                    
                    print("\n")
              
        elif choice == "4":
            print("\n===== RECENT EVENTS LOG =====")
            logs_to_show = min(20, len(self.events_log))
            for log in self.events_log[-logs_to_show:]:
                print(log)
              
        elif choice == "5":
            print("\n===== EQUIPMENT SUMMARY =====")
            all_equipment = {}
            
            # Count all equipment across all soldiers
            for soldier in self.soldiers:
                for item, qty in soldier.equipment.items():
                    if item in all_equipment:
                        all_equipment[item] += qty
                    else:
                        all_equipment[item] = qty
            
            if not all_equipment:
                print("No equipment found")
            else:
                for item, qty in all_equipment.items():
                    info = self.equipment_database.get(item, {})
                    weight = info.get("weight", "N/A")
                    effectiveness = info.get("effectiveness", "N/A")
                    
                    print(f"- {item}: {qty} units (Weight: {weight}, Effectiveness: {effectiveness})")
              
        elif choice == "6":
            print("\n===== PERSONNEL STATUS =====")
            if not self.soldiers:
                print("No personnel found")
            else:
                status_groups = {}
                for soldier in self.soldiers:
                    if soldier.status not in status_groups:
                        status_groups[soldier.status] = []
                    status_groups[soldier.status].append(soldier)
                
                for status, soldiers in status_groups.items():
                    print(f"\n{status} Personnel ({len(soldiers)}):")
                    for soldier in soldiers:
                        print(f"- {soldier.rank} {soldier.name}, Health: {soldier.health}%")
              
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the simulator interface"""
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                self.soldier_menu()
            elif choice == "2":
                self.team_menu()
            elif choice == "3":
                self.mission_menu()
            elif choice == "4":
                self.simulation_menu()
            elif choice == "5":
                self.reports_menu()
            elif choice == "6":
                print("Exiting simulator...")
                break
            else:
                print("Invalid choice")


# Sample data
def create_sample_data(simulator):
    # Create soldiers
    s1 = simulator.create_soldier("Johnson", rank="Sergeant", location=(10, 10))
    s2 = simulator.create_soldier("Smith", rank="Corporal", location=(12, 10))
    s3 = simulator.create_soldier("Williams", rank="Medic", location=(8, 10))
    s4 = simulator.create_soldier("Miller", rank="Private", location=(10, 12))
    s5 = simulator.create_soldier("Davis", rank="Private", location=(10, 8))
    s6 = simulator.create_soldier("Garcia", rank="Sergeant", location=(20, 20))
    s7 = simulator.create_soldier("Wilson", rank="Corporal", location=(22, 20))
    s8 = simulator.create_soldier("Taylor", rank="Private", location=(20, 22))
    
    # Add equipment
    s1.add_equipment("Rifle", 1)
    s1.add_equipment("Ammo", 5)
    s2.add_equipment("Radio", 1)
    s2.add_equipment("Pistol", 1)
    s3.add_equipment("Medkit", 3)
    s3.add_equipment("Water", 2)
    s4.add_equipment("Binoculars", 1)
    s4.add_equipment("Ammo", 3)
    s5.add_equipment("Rifle", 1)
    s5.add_equipment("Grenade", 2)
    s6.add_equipment("Rifle", 1)
    s6.add_equipment("Night Vision", 1)
    s7.add_equipment("Radio", 1)
    s7.add_equipment("Ammo", 4)
    s8.add_equipment("Rifle", 1)
    s8.add_equipment("Rations", 3)
    
    # Create teams
    alpha = simulator.create_team("Alpha")
    bravo = simulator.create_team("Bravo")
    
    # Add members to teams
    alpha.add_member(s1)
    alpha.add_member(s2)
    alpha.add_member(s3)
    alpha.add_member(s4)
    alpha.add_member(s5)
    bravo.add_member(s6)
    bravo.add_member(s7)
    bravo.add_member(s8)
    
    # Set commanders
    alpha.set_commander(s1)
    bravo.set_commander(s6)
    
    # Create missions
    recon = simulator.create_mission("Eagle Eye", "Reconnaissance of enemy territory", (50, 60))
    recon.set_difficulty(3)
    recon.add_objective("Reach observation point")
    recon.add_objective("Gather intelligence")
    recon.add_objective("Document enemy movements")
    recon.add_objective("Return to base")
    
    assault = simulator.create_mission("Hammer Strike", "Clear enemy outpost", (80, 30))
    assault.set_difficulty(7)
    assault.add_objective("Secure perimeter")
    assault.add_objective("Neutralize enemy forces")
    assault.add_objective("Secure objective")
    assault.add_objective("Extract intel")
    assault.add_objective("Withdraw from area")
    
    # Assign teams to missions
    recon.add_team(alpha)
    alpha.assign_team_mission(recon.name)
    
    assault.add_team(bravo)
    bravo.assign_team_mission(assault.name)
    
    # Simulate some progress
    recon.update_status("Active")
    recon.complete_objective(0)
    recon.log_event("Team Alpha reached observation point")
    
    simulator.log_event("Sample data created successfully")
    return simulator


# Main execution
if __name__ == "__main__":
    simulator = MilitarySimulator()
    
    # Ask if user wants sample data
    print("Military Simulator")
    use_sample = input("Would you like to load sample data? (y/n): ").lower()
    
    if use_sample == 'y':
        simulator = create_sample_data(simulator)
        print("Sample data loaded!")
    
    # Run the simulator interface
    simulator.run()