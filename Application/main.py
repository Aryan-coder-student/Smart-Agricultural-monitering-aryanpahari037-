import flet as ft
import os
import requests
from features import mixed
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def main(page: ft.Page):
    # Set basic properties
    page.title = "AgriTech 2.0"
    page.window.width = 380        
    page.window.height = 750
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 3
    page.window.resizable = False
    page.bgcolor = "#3AB09E"
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }

    def create_button(text, icon, route):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icon, color="#006400"), 
                    ft.Text(
                        text,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.W_700  
                    )
                ],
                alignment=ft.MainAxisAlignment.START,  
            ),
            bgcolor="#A2D9CE",
            padding=10,
            border_radius=5,
            width=400,  # Full width
            ink=True,
            on_click=lambda _: page.go(route)
        )

    # Define home page
    def home_page(page):
        
        page.clean()
        
        text = ft.Text(
            value="🌾 AgriTech 2.0",
            color=ft.colors.GREEN,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL
        )
        text.style = ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        
        # Adding buttons
        crop_pred_button = create_button("Crop Recommendation", "eco", "/crop_recommendation")
        irrigation_sch = create_button("Irrigation Checking", "water_drop", "/irrigation_checking")
        fertility_check = create_button("Fertility Checking", "agriculture", "/fertility_checking")
        Mixed_cropping = create_button("Mixed Cropping", "crop", "/mixed_cropping")
        about = create_button("About App", "info", "/about_app")

        button_column = ft.Column(
            controls=[
                crop_pred_button,
                irrigation_sch,
                fertility_check,
                Mixed_cropping,
                about
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START  # Align buttons to the start (left)
        )

        # Adding an image
        img = ft.Image(
            src="Images Agri Tech/Intro Page.jpg",
            width=400,
            fit=ft.ImageFit.CONTAIN,
        ) 
        
        img.border_radius = ft.border_radius.only(40, 40)

        container = ft.Container(
            content=ft.Column([
                text,
                ft.Container(height=50),
                button_column
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),  
            bgcolor="#FFFFFFCC",  # Semi-transparent white background
            height=495,
            width=400,
            padding=40
        )
        container.border_radius = ft.border_radius.only(top_left=20, top_right=20, bottom_left=40, bottom_right=40)
        page.add(img, container)
        page.bgcolor = "#3AB09E"
        page.update()  
    def crop_recommendation_page(page,connected = False):
        page.bgcolor = "#FFFFFFCC"
        page.clean() 
        page.add(ft.Column(controls = [ft.Text("Crop Recomendation Page",
            color=ft.colors.GREEN,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL)] , alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10))
        
        if connected:
            icon_name = "check_circle"
            message = "Sensors are connected."
            icon_color = ft.colors.GREEN
            text_color = ft.colors.GREEN      
        else:
            icon_name = "error"
            message = "Sensors are not connected yet."
            icon_color = ft.colors.RED
            text_color = ft.colors.RED
        error_message = ft.Row(
            controls=[
                ft.Icon(name=icon_name, color=icon_color),
                ft.Text(
                    value=message,
                    color=text_color,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        page.add(error_message)

        input_fields = {
        "Nitrogen": ft.TextField(label="Nitrogen (kg/ha)", width=160, color=ft.colors.BLACK),
        "Phosphorus": ft.TextField(label="Phosphorus (kg/ha)", width=160, color=ft.colors.BLACK),
        "Potassium": ft.TextField(label="Potassium (kg/ha)", width=160, color=ft.colors.BLACK),
        "Temperature": ft.TextField(label="Temperature (°C)", width=160, color=ft.colors.BLACK),
        "Humidity": ft.TextField(label="Humidity (%)", width=160, color=ft.colors.BLACK),
        "pH": ft.TextField(label="pH", width=160, color=ft.colors.BLACK),
        "Rainfall": ft.TextField(label="Rainfall (mm)", width=160, color=ft.colors.BLACK)
        }
        if connected:
            input_fields["Nitrogen"].value = 90
            input_fields["Phosphorus"].value = 42
            input_fields["Potassium"].value = 43
            input_fields["Temperature"].value = 20.87
            input_fields["Humidity"].value = 82.00
            input_fields["pH"].value = 6.50
            input_fields["Rainfall"].value = 202.93

        left_column = ft.Column(controls=[
                input_fields["Nitrogen"],
                input_fields["Phosphorus"],
                input_fields["Potassium"],
                input_fields["Temperature"]
            ])
        right_column = ft.Column(controls=[
                input_fields["Humidity"],
                input_fields["pH"],
                input_fields["Rainfall"]
            ])
        
        def submit_data(e):
            input_features = {key: field.value for key, field in input_fields.items()}
            try:
                Nitrogen = input_features["Nitrogen"]
                Phosphorus = input_features["Phosphorus"]
                Potassium = input_features["Potassium"]
                Temperature = input_features["Temperature"]
                Humidity = input_features["Humidity"]
                pH = input_features["pH"]
                Rainfall = input_features["Rainfall"]

                df_data = {"Nitrogen": float(Nitrogen),
                           "Phosphorus": float(Phosphorus),
                           "Potassium": float(Potassium),
                           "Temperature": float(Temperature),
                           "Humidity":float(Humidity),
                            "pH": float(pH),
                            "Rainfall": float(Rainfall)}
                output = ft.Text("",
                        color=ft.colors.BROWN_700,
                        font_family="RobotoSlab",
                        weight=ft.FontWeight.W_200,
                        text_align=ft.TextAlign.CENTER,
                        theme_style=ft.TextThemeStyle.DISPLAY_SMALL
                        )
                url = "http://127.0.0.1:8000/crop/predict_crop/"
                x = requests.post(url, json=df_data)
                page.snack_bar = ft.SnackBar(ft.Text("Data submitted successfully!"))
                output.value = f"{x.text} can be grown in this area."                
                page.add(output)
            except ValueError as ve:
                print(f"Input error: {ve}")
                page.snack_bar = ft.SnackBar(ft.Text("Invalid input! Please enter numeric values."), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()

        form_row = ft.Row(controls=[left_column, right_column],alignment=ft.MainAxisAlignment.CENTER,spacing=10)
        page.add(form_row)
        if not connected :
            page.add(ft.Row(
                controls=[ft.ElevatedButton("Back to Home", on_click=lambda _: page.go("/"),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                          ft.ElevatedButton("Refresh",  on_click=lambda _: (crop_recommendation_page(page=page,connected=True),page.go("/crop_recommendation")),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE)],
                alignment=ft.MainAxisAlignment.CENTER
            ))
            
        elif connected :
            page.add(ft.Row(
                controls=[ft.ElevatedButton("Back to Home", on_click=lambda _: page.go("/"),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                          ft.ElevatedButton("Submit", on_click=submit_data, bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                          ft.ElevatedButton("Refresh", on_click=lambda _: (crop_recommendation_page(page=page,connected=True),page.go("/crop_recommendation")),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE)],
                alignment=ft.MainAxisAlignment.CENTER
            ))
        page.update()

    
    def irrigation_checking_page(page,connected = False):
        page.bgcolor = "#FFFFFFCC"
        page.clean()
        page.add(ft.Text("Irrigation Checking Page",
            color=ft.colors.GREEN,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL))
        
        if connected:
            icon_name = "check_circle"
            message = "Sensors are connected."
            icon_color = ft.colors.GREEN
            text_color = ft.colors.GREEN
        else:
            icon_name = "error"
            message = "Sensors are not connected yet."
            icon_color = ft.colors.RED
            text_color = ft.colors.RED
        error_message = ft.Row(
            controls=[
                ft.Icon(name=icon_name, color=icon_color),
                ft.Text(
                    value=message,
                    color=text_color,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        crop_type  = {
            'Coffee': 0,
            'Garden Flowers': 1,
            'Groundnuts': 2,
            'Maize': 3,
            'Paddy': 4,
            'Potato': 5,
            'Pulse': 6,
            'Sugarcane': 7,
            'Wheat': 8
            }

        input_fields = {
            "CropType": ft.Dropdown(
                        label="Crop",
                        options=[ft.dropdown.Option(crop) for crop in crop_type],
                        width=160, 
                        color=ft.colors.BLACK,bgcolor = ft.colors.GREY_50
                        ),
            "CropDays": ft.TextField(label="Crop Days", width=160, color=ft.colors.BLACK),
            "SoilMoisture": ft.TextField(label="Soil Moisture", width=160, color=ft.colors.BLACK),
            "temperature": ft.TextField(label="Temperature", width=160, color=ft.colors.BLACK),
            "Humidity": ft.TextField(label="Humidity", width=160, color=ft.colors.BLACK)
            }
        
        if connected:
            input_fields["CropType"].value = list(crop_type.keys())[8]
            input_fields["CropDays"].value = 10
            input_fields["SoilMoisture"].value = 400
            input_fields["temperature"].value = 30
            input_fields["Humidity"].value = 15
        ouput = ft.Text("",
            color=ft.colors.GREEN,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_200,
            text_align=ft.TextAlign.CENTER,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL
            )
        def submit_data(e):
            input_features = {key: field.value for key, field in input_fields.items()}
            try:
                CropType = crop_type[input_features["CropType"]]
                CropDays = input_features[ "CropDays"]
                SoilMoisture = input_features["SoilMoisture"]
                temperature = input_features["temperature"]
                Humidity = input_features["Humidity"]
                url = "http://127.0.0.1:8000/irrigation/predict_irrigation"
                df_data = {
                    "CropType": int(CropType),
                    "CropDays": int(CropDays),
                    "SoilMoisture": int(SoilMoisture),
                    "Temperature": int(temperature),
                    "Humidity": int(Humidity)
                }
                
                # print(df_data)
                x = requests.post(url, json = df_data)
                ouput.value = ""
                print(x.text)
                if int(x.text) == 1:
                    ouput.value = "Field is not irrigated , Irrigation required"
                    ouput.color = ft.colors.RED
                elif int(x.text)==0:
                    ouput.value = "Field is irrigated , Irrigation not required"
                    ouput.color = ft.colors.GREEN
                page.snack_bar = ft.SnackBar(ft.Text("Data submitted successfully!"))

                
            except ValueError as ve:
                print(f"Input error: {ve}")
                page.snack_bar = ft.SnackBar(ft.Text("Invalid input! Please enter numeric values."), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
            page.add(ouput)
            
        left_column = ft.Column(controls=[
            input_fields["CropType"],
            input_fields["CropDays"],
            input_fields["SoilMoisture"],
        ])
        right_column = ft.Column(controls=[
            input_fields["temperature"],
            input_fields["Humidity"],

        ])
        page.add(error_message)
        page.add(ft.Row(controls=[left_column, right_column],alignment=ft.MainAxisAlignment.CENTER,spacing=10))
        if connected:
            page.add(ft.Row(
                controls=[ft.ElevatedButton("Submit", on_click=submit_data,bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                          ft.ElevatedButton("Home", on_click=lambda _: page.go("/"),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                          ft.ElevatedButton("Refresh", on_click=lambda _: (irrigation_checking_page(page = page , connected=True),page.go("/irrigation_checking")),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE)],
                alignment=ft.MainAxisAlignment.CENTER
            ))
        else:
            page.add(ft.Row(controls = [ft.ElevatedButton("Home", on_click=lambda _: page.go("/"),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                                       ft.ElevatedButton("Refresh", on_click=lambda _: (irrigation_checking_page(page = page , connected=True)),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE) ],alignment=ft.MainAxisAlignment.CENTER))
        
        page.update()

    def fertility_checking_page(page,connected=True):
        page.bgcolor = "#FFFFFFCC"
        page.clean()
        page.add(ft.Text("Fertility Checking Page",
            color=ft.colors.GREEN,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL))
        if connected:
            icon_name = "check_circle"
            message = "Sensors are connected."
            icon_color = ft.colors.GREEN
            text_color = ft.colors.GREEN
        else:
            icon_name = "error"
            message = "Sensors are not connected yet."
            icon_color = ft.colors.RED
            text_color = ft.colors.RED

        error_message = ft.Row(
            controls=[
                ft.Icon(name=icon_name, color=icon_color),
                ft.Text(
                    value=message,
                    color=text_color,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        page.add(error_message)
        
        input_fields = {
                    "N": ft.TextField(label="Nitrogen (N) in ppm", width=160, color=ft.colors.BLACK ),
                    "P": ft.TextField(label="Phosphorus (P) in ppm", width=160, color=ft.colors.BLACK ),
                    "K": ft.TextField(label="Potassium (K) in ppm", width=160, color=ft.colors.BLACK ),
                    "pH": ft.TextField(label="pH", width=160, color=ft.colors.BLACK ),
                    "EC": ft.TextField(label="Electrical Conductivity (EC) in dS/m", width=160, color=ft.colors.BLACK ),
                    "OC": ft.TextField(label="Organic Carbon (OC) in %", width=160, color=ft.colors.BLACK ),
                    "S": ft.TextField(label="Sulfur (S) in ppm", width=160, color=ft.colors.BLACK ),
                    "Zn": ft.TextField(label="Zinc (Zn) in ppm", width=160, color=ft.colors.BLACK ),
                    "Fe": ft.TextField(label="Iron (Fe) in ppm", width=160, color=ft.colors.BLACK ),
                    "Cu": ft.TextField(label="Copper (Cu) in ppm", width=160, color=ft.colors.BLACK ),
                    "Mn": ft.TextField(label="Manganese (Mn) in ppm", width=160, color=ft.colors.BLACK ),
                    "B": ft.TextField(label="Boron (B) in ppm", width=160, color=ft.colors.BLACK )
                }
        if connected:
            input_fields['N'].value = 138
            input_fields['P'].value = 45
            input_fields['K'].value = 210
            input_fields['pH'].value = 6.5
            input_fields['EC'].value = 1.2
            input_fields['OC'].value = 0.75
            input_fields['S'].value = 10
            input_fields['Zn'].value = 1.5
            input_fields['Fe'].value = 4.5
            input_fields['Cu'].value = 0.5
            input_fields['Mn'].value = 3.0
            input_fields['B'].value = 0.8
        ouput = ft.Text("",
            color=ft.colors.GREEN,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_200,
            text_align=ft.TextAlign.CENTER,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL
            )
        
        def submit_data(e):
            input_features = {key: field.value for key, field in input_fields.items()}
            try:
                N =input_features["N"]
                P = input_features["P"]
                K = input_features["K"]
                pH = input_features["pH"]
                EC = input_features["EC"]
                OC = input_features["OC"]
                S = input_features["S"]
                Zn = input_features["Zn"]
                Fe = input_features["Fe"]
                Cu = input_features["Cu"]
                Mn = input_features["Mn"]
                B = input_features["B"]

                url = "http://127.0.0.1:8000/fertility/predict_fertility/"

                df_data = {
                    "N": float(N),
                    "P": float(P),
                    "K": float(K),
                    "pH": float(pH),
                    "EC": float(EC),
                    "OC": float(OC),
                    "S": float(S),
                    "Zn": float(Zn),
                    "Fe": float(Fe),
                    "Cu": float(Cu),
                    "Mn": float(Mn),
                    "B": float(B)
                }
                x = requests.post(url, json=df_data)
                prediction = int(x.text)
                if prediction == 0:
                    ouput.value = "Fertility of the soil is very low, fertilizers are required"
                    ouput.color = ft.colors.RED
                elif prediction == 1:
                    ouput.value = "Fertility of the soil is considerable"
                    ouput.color = ft.colors.BROWN_400
                elif prediction == 2:
                    ouput.value = "Fertility of the soil is high, fertilizers are not required"
                    ouput.color = ft.colors.GREEN
                page.snack_bar = ft.SnackBar(ft.Text("Data submitted successfully!"))
                    

            except ValueError as ve:
                print(f"Input error: {ve}")
                page.snack_bar = ft.SnackBar(ft.Text("Invalid input! Please enter numeric values."), bgcolor=ft.colors.RED)
            except Exception as ex:
                print(f"Unexpected error: {ex}")
                page.snack_bar = ft.SnackBar(ft.Text("An unexpected error occurred."), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()
            page.add(ouput)
                
        left_column = ft.Column(controls=[
            input_fields["N"],
            input_fields["P"],
            input_fields["K"],
            input_fields["pH"],
            input_fields["EC"],
            input_fields["OC"],
        ])
        right_column = ft.Column(controls=[
            input_fields["S"],
            input_fields["Zn"],
            input_fields["Fe"],
            input_fields["Cu"],
            input_fields["Mn"],
            input_fields["B"],
        ])
        
        page.add(ft.Row(controls=[left_column, right_column],  alignment=ft.MainAxisAlignment.CENTER,spacing=10))
        if connected:
            page.add(ft.Row(
                controls=[ft.ElevatedButton("Submit", on_click=submit_data,bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                          ft.ElevatedButton("Home", on_click=lambda _: page.go("/"),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                          ft.ElevatedButton("Refresh", on_click=lambda _: (fertility_checking_page(page = page),page.go("/fertility_checking")),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE)],
                alignment=ft.MainAxisAlignment.CENTER
            ))
        else:
            page.add(ft.Row(controls=[ft.ElevatedButton("Home", on_click=lambda _: page.go("/"),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE),
                     ft.ElevatedButton("Refresh", on_click=lambda _: (fertility_checking_page(page = page),page.go(page.route)),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE)],alignment=ft.MainAxisAlignment.CENTER)
                     )
        page.add(ouput)
        page.update()

    def mixed_cropping(page):
        API_KEY = os.getenv("API_KEY")  
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-pro")
        page.scroll = ft.ScrollMode.AUTO
        page.window.width = 900
        page.window.height = 750
        page.clean()
        page.bgcolor = "#FFFFFFCC"

        page.add(ft.Text("Mixed Cropping or Multiple cropping",
            color=ft.colors.GREEN,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
            theme_style=ft.TextThemeStyle.DISPLAY_SMALL))

        page.add(ft.Text("The concept of mixed cropping involves growing two or more crops together to optimize land use and improve yield. Choose a crop from the list below to explore mixed cropping possibilities.",
                color=ft.colors.BROWN,
            font_family="RobotoSlab",
            text_align=ft.TextAlign.CENTER))

        loading_spinner = ft.ProgressRing(width=50, height=50)
        loading_container = ft.Container(
            content=loading_spinner,
            alignment=ft.alignment.center,
            visible=False
        )
        page.add(loading_container)

        crop_list = [
            'Rice', 'Maize', 'Chickpea', 'Kidney Beans', 'Pigeon Peas', 'Moth Beans',
            'Mung Bean', 'Black Gram', 'Lentil', 'Pomegranate', 'Banana', 'Mango',
            'Grapes', 'Watermelon', 'Muskmelon', 'Apple', 'Orange', 'Papaya',
            'Coconut', 'Cotton', 'Jute', 'Coffee'
        ]

        content = ft.Column()

        def on_crop_change(e):
            content.controls.clear()
            loading_container.visible = True  # Show loading spinner
            page.update()
            option = selected_crop.value
            if option:
                content.controls.append(
                    ft.Markdown(f"<h5> Mixed Cropping with <u>{option}</u> </h5>", extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)
                )
                mixed_crop_objects = mixed.MixedCroping(option)
                j = 1
                for i in mixed_crop_objects.mixed_crop():
                    res = model.generate_content(f"ratio of seedling for mixed cropping of {option} and {i}")
                    generated_text = res._result.candidates[0].content.parts[0].text
                    content.controls.append(ft.Markdown(f"**{j}.) {i}**", extension_set=ft.MarkdownExtensionSet.GITHUB_WEB))
                    content.controls.append(ft.Markdown(f"{generated_text}", extension_set=ft.MarkdownExtensionSet.GITHUB_WEB))
                    
                    crop_info = mixed_crop_objects.crop_info(i)
                    if isinstance(crop_info, pd.Series):
                        crop_info = crop_info.to_frame().T  # Convert Series to DataFrame

                    content.controls.append(ft.DataTable(
                        columns=[ft.DataColumn(ft.Text(col)) for col in crop_info.columns],
                        rows=[
                            ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row])
                            for row in crop_info.values
                        ]
                    ))
                    content.controls.append(ft.Markdown("<hr>", extension_set=ft.MarkdownExtensionSet.GITHUB_WEB))
                    j += 1
                loading_container.visible = False  # Hide loading spinner
                page.update()

        selected_crop = ft.Dropdown(
            options=[ft.dropdown.Option(crop) for crop in crop_list],
            width=300,
            on_change=on_crop_change,
        )
        page.add(selected_crop)
        page.add(content)
        page.update()
        page.add(ft.ElevatedButton("Back to Home", on_click=lambda _: page.go("/"),bgcolor=ft.colors.GREEN_700,color=ft.colors.WHITE))
        
    def about_app_page(page):
        page.clean()
        
        page.add(ft.Text("About App Page"))
        page.add(ft.ElevatedButton("Back to Home", on_click=lambda _: page.go("/")))
        page.update()

    
    def route_change(event):
        if event.route == "/":
            page.window.width = 380        
            page.window.height = 750
            home_page(page)
        elif event.route == "/crop_recommendation":
            crop_recommendation_page(page)
        elif event.route == "/irrigation_checking":
            irrigation_checking_page(page)
        elif event.route == "/fertility_checking":
            fertility_checking_page(page)
        elif event.route == "/mixed_cropping":
            mixed_cropping(page)
        elif event.route == "/about_app":
            about_app_page(page)

    page.on_route_change = route_change

    page.go("/")

# Run the app
ft.app(target=main)
