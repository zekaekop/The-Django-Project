from django.shortcuts import render, redirect
from accounts.models import UserProfile
from dataclasses import dataclass
from accounts.views import decrease_BZ

import random

def authenticate_users(request):
    if not request.user.is_authenticated:
        raise Http404()

class PfpAssembly():

    def pfp_regen_debug(self, request):
        authenticate_users(request)
        result = self.create_user_pfp(request.user)
        return redirect("/profile/" + request.user.username)

    def pfp_reroll(self, request): # we could add a currency that costs to reroll, it adds value
        authenticate_users(request)
        result = self.create_user_pfp(request.user)
        decrease_BZ(request, 20)
        return redirect("/profile/" + request.user.username)

    def create_user_pfp(self, user, new_user = None):
        # generate pfp
        generated_pic_data = self.generate_pfp_values(4, 4)
        # Try to get existing profile or create new one
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.generated_pic = generated_pic_data
        profile.save()

    # class Pixel: # I removed this since i forgot the model uses JSONField meaning its just way easier to do a dict
    #     def __init__(self, r, g, b, a=255):
    #         self.color = [r, g, b, a]
    #         self.effects = []
    #         self.gradience = None
    #         self.scale = 1
    #         self.roundness = 0

    #     def add_effect(self, effect_name, **kwargs):
    #         self.effects.append(effect_name)
    #         for key, value in kwargs.items():
    #             setattr(self, key, value)

    def write_pfp(self, pfp):

        generated_pic = []

        for y in range(pfp.height):
            row = []
            for x in range(pfp.width):

                pixel = {
                    "color": [0,0,0,0],
                    "gradience": [],
                    "glow": [],
                    "scale": 1,
                    "roundness":0,
                    "rotation":0,
                }

                if random.choice([True, False]): # random 50% 50% to block color or not

                    # pixel = self.Pixel(pfp.red, pfp.blue, pfp.green, 255)
                    pixel["color"] = [pfp.red, pfp.blue, pfp.green, 255]

                    if pfp.gradience_chance == 1:
                        pixel["gradience"] = [pfp.red_gradience, pfp.blue_gradience, pfp.green_gradience]

                    if pfp.glow_chance == 1: # you can apply more affects using add_affect, you just need a tag
                        pixel["glow"] = [pfp.glow_intensity, pfp.glow_radius]

                    if pfp.roundness_chance == 1:
                        pixel["roundness"] = pfp.roundness
                    
                    if pfp.scale_chance == 1:
                        pixel["scale"] = pfp.scale_size

                    if pfp.rotation_chance == 1:
                        pixel["rotation"] = pfp.rotation

                    row.append(pixel)

                else:
                    row.append(pixel) # Emty gray pixel
            generated_pic.append(row)

        return generated_pic

    def generate_pfp_values(self ,height = 4, width = 4): # its 4 by 4 and than it gets mirrored and flipped on the other sides 

        # Each block on the PFP is a div with its own styles
        # we create a array for each block holding the needed values like RGB glow gradience etc...
        # for the PFP there is a small chance for them to get special values that add to their rarity
        # in the future i will make them tradeable /// reach


        # TLDR its a 2D array holding each blocks needed value
        
        @dataclass
        class pfp_values:
            height: int = 4 # default 4
            width: int = 4 

            # rainbow_chance: int =  random.randint(0,100)

            red: int = random.randint(128,255)
            green: int = random.randint(128,255)
            blue: int = random.randint(128,255)

            red_gradience: int = random.randint(0,255)
            blue_gradience: int = random.randint(0,255)
            green_gradience: int = random.randint(0,255)

            scale_size: int = random.uniform(0.5,1.5)
            scale_chance: int = random.randint(0,5)
            glow_chance: int = random.randint(0,5)
            gradience_chance: int = random.randint(0,5)
            roundness_chance: int = random.randint(0,5)
            rotation_chance:int = random.randint(0,5)

            roundness: int = random.randint(1,30)
            glow_intensity: int = random.randint(5,30) # the glow is just an drop shadow thats bright
            glow_radius: int = random.randint(10,30)
            rotation: int = random.randint(0,360)
            # individuality: int = random.randint(0,30)
        
        pfp_values.height = height
        pfp_values.width = width

        generated_pic = self.write_pfp(pfp_values)

        return generated_pic