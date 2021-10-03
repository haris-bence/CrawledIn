import os
import PIL.Image
from selenium import webdriver
from PIL import Image
import wget

# Open .txt that contains the company names
with open("./on_confee.txt", "r") as f:
    lines = f.readlines()
    i = len(lines)-1
    while i != -1:
        # Converting raw company names to more "linkedin style" strings
        line = lines[i]
        without = line.split("\n")
        line = without[0]
        line = line.lower()
        if line.__contains__(" "):
            tort = line.split(" ")
            line = tort[0] + "-" + tort[1]
        if line.__contains__("."):
            tort = line.split(".")
            line = tort[0] + tort[1]
        if line.__contains__(","):
            tort = line.split(",")
            line = tort[0] + tort[1]
        if line.__contains__("&"):
            tort = line.split("&")
            line = tort[0] + tort[1]
        if line.__contains__("/"):
            tort = line.split("/")
            line = tort[0] + tort[1]
        # Using Edge Driver to automate tasks
        # Define the proper location
        browser = webdriver.Edge('C:/path_to_executable')
        try:
            browser.get("https://linkedin.com/company/" + line)
            print("Working on "+line)
            # Searching src attributes for both profile and banner pictures
            profile_pic = browser.find_element_by_class_name('artdeco-entity-image').get_attribute('src')
            cover = browser.find_element_by_class_name('cover-img__image').get_attribute('src')
            path_long_profile = profile_pic.split("?")
            path_long_cover = cover.split("?")
            path_short_profile = path_long_profile[0].split("/", -1)
            path_short_cover = path_long_cover[0].split("/", -1)
            # Download images with the names defined above
            profile_download = wget.download(profile_pic)
            cover_download = wget.download(cover)
            company = "./" + line
            profile_pic_name = company + "/" + line + '1.jfif'
            cover_pic_name = company + "/" + line + '2.jfif'
            # Make folder for each company, with the pics and description inside
            os.mkdir(company)
            os.rename('./' + path_short_profile[-1], profile_pic_name)
            os.rename('./' + path_short_cover[-1], cover_pic_name)
            image = Image.open(profile_pic_name)
            image = image.resize((400, 400), PIL.Image.NEAREST)
            image.save(profile_pic_name)
            print(cover)
            try:
                # Saving the description into a company named .txt
                description = browser.find_element_by_class_name('about-us__description').text
                file = company + "/" + line + ".txt"
                with open(file, "w") as g:
                    print(description, file=g)
                print("All parameters found for " + line)
            except:
                # Sometimes a description isn't available
                print("NO DESCRIPTION FOR "+line)
            i = i - 1
        except:
            # Neither is a company
            print("NO SUCH COMPANY AS "+line+", SKIP")
            i = i - 1
