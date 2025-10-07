import os

class Character:
    def __init__(self, config_directory: str = "characters/config", character_name: str = "shadowheart"):
        self.config_path = config_directory 
        self.audio_sample_path = None
        self.description: str = None
        self.name: str = None
        self.__set_character(character_name=character_name)
    
    def __set_character(self, character_name: str):
        character_path = os.path.join(self.config_path, character_name)

        if not os.path.exists(character_path):
            raise ValueError(f"Character config not found: {character_path}")
        
        # check if character has both an audio and a text config file
        audio_config_path = os.path.join(character_path, "audio.wav")
        text_config_path = os.path.join(character_path, "description.md")
        
        if not os.path.exists(audio_config_path):
            raise ValueError(f"Character config incomplete for {character_path}, missing audio.wav")
        if not os.path.exists(text_config_path):
            raise ValueError(f"Character config incomplete for {character_path}, missing description.md")
        
        print("character config found!")
        self.audio_sample_path = audio_config_path
        with open(text_config_path, "r") as f:
            self.description = f.read()
        print("character description loaded!")
        self.name = character_name




        

        


    
        