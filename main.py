import os
from tkinter import Tk, Label, Frame, Entry, messagebox, PhotoImage, Canvas


class RoundedButton(Canvas):
    """Класс для создания закругленных кнопок"""

    def __init__(self, master=None, text="", radius=40, bg="green", fg="white",
                 active_bg="dark green", active_fg="black", command=None, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.config(bg=master.cget("bg"))
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.active_bg = active_bg
        self.active_fg = active_fg
        self.command = command
        self.text = text
        self.is_active = False
        # Обработка событий
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        # Отрисовка кнопки
        self.draw_button()

    def draw_button(self):
        """Отрисовывает закругленную кнопку"""
        self.delete("all")
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        # Рисуем закругленный прямоугольник
        bg_color = self.active_bg if self.is_active else self.bg
        self.create_rounded_rect(0, 0, width, height, radius=self.radius, fill=bg_color, outline="")
        # Добавляем текст
        fg_color = self.active_fg if self.is_active else self.fg
        self.create_text(width // 2, height // 2, text=self.text, fill=fg_color, font=("Arial", 14))

    def _on_click(self, event):
        """Обработчик нажатия на кнопку"""
        if self.command:
            self.command()

    def _on_enter(self, event):
        """Обработчик наведения курсора"""
        self.is_active = True
        self.draw_button()  # Перерисовываем кнопку с активными цветами

    def _on_leave(self, event):
        """Обработчик ухода курсора"""
        self.is_active = False
        self.draw_button()  # Перерисовываем кнопку с исходными цветами


# Добавляем метод create_rounded_rect в Canvas
def create_rounded_rect(self, x1, y1, x2, y2, radius=40, **kwargs):
    """Создает закругленный прямоугольник на Canvas"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)


Canvas.create_rounded_rect = create_rounded_rect


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Гуляй, Вася!")
        self.geometry(self.center_window(400, 830))  # Устанавливаем размеры и центрируем окно
        self.frames = {}
        self.current_frame = None
        self.images = {}  # Словарь для хранения изображений
        # Создаем папку для изображений, если её нет
        if not os.path.exists("images"):
            os.makedirs("images")
            print("Создана папка images. Поместите туда ваши изображения.")
        # Загрузка изображений
        self.load_images()
        # Создание всех фреймов
        self.create_frames()
        # Показываем начальный экран
        self.show_frame("Registration")
        # Привязка клавиши Esc к выходу из приложения
        self.bind("<Escape>", self.exit_app)

    def load_images(self):
        """Загружает все PNG изображения из папки images"""
        try:
            for filename in os.listdir("images"):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    name = os.path.splitext(filename)[0]
                    try:
                        img = PhotoImage(file=os.path.join("images", filename))
                        self.images[name] = img
                        print(f"Успешно загружено: {filename}")
                    except Exception as e:
                        print(f"Ошибка загрузки {filename}: {str(e)}")
        except Exception as e:
            print(f"Общая ошибка при загрузке изображений: {str(e)}")

    def create_frames(self):
        """Создает все фреймы приложения"""
        self.create_frame("Registration", self.create_registration_ui)
        self.create_frame("log_in_to_the_app", self.create_login_ui)
        self.create_frame("choose_a_situation", self.create_choose_a_situation_ui)
        self.create_frame("Save_me_from_my_boss", self.create_save_me_from_my_boss_ui)
        self.create_frame("required_time", self.create_required_time_ui)
        self.create_frame("I_m_not_going_to_work_on_Saturday", self.create_saturday_ui)
        self.create_frame("To_a_bar_with_friends", self.create_bar_ui)
        self.create_frame("Feedback_end", self.create_feedback_ui)
        self.create_frame("Phone_loss", self.create_phone_loss_ui)
        self.create_frame("settings", self.create_settings_ui)

    def create_frame(self, name, setup_func):
        """Создает фрейм с указанной функцией настройки"""
        frame = Frame(self)
        self.frames[name] = frame
        setup_func(frame)

    def show_frame(self, frame_name):
        """Показывает указанный фрейм"""
        if frame_name not in self.frames:
            print(f"Фрейм {frame_name} не найден!")
            return
        if self.current_frame:
            self.current_frame.pack_forget()
        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def exit_app(self, event):
        """Закрывает приложение при нажатии клавиши Esc"""
        self.destroy()

    def center_window(self, width, height):
        """Вычисляет координаты для размещения окна по центру экрана"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        return f"{width}x{height}+{x}+{y}"

    def create_registration_ui(self, frame):
        """Настройка UI для экрана регистрации"""
        if "Registration" in self.images:
            bg_label = Label(frame, image=self.images["Registration"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        RoundedButton(
            frame,
            text="Регистрация",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            radius=25,
            command=lambda: self.show_frame("log_in_to_the_app"),
            width=300,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_login_ui(self, frame):
        """Настройка UI для входа"""
        if "log_in_to_the_app" in self.images:
            bg_label = Label(frame, image=self.images["log_in_to_the_app"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Поле ввода телефона
        phone_entry = Entry(frame, font=("Arial", 12))
        phone_entry.place(relx=0.6, rely=0.72, anchor="center", width=165, height=15)
        # Поле ввода кода из SMS
        sms_entry = Entry(frame, font=("Arial", 12))
        sms_entry.place(relx=0.55, rely=0.78, anchor="center", width=75, height=15)
        # Функция отправки кода
        def send_sms_code():
            phone = phone_entry.get().strip()
            if not phone:
                messagebox.showerror("Ошибка", "Введите номер телефона")
            else:
                sms_entry.delete(0, "end")
                sms_entry.insert(0, "1515")  # Имитация отправки кода
                messagebox.showinfo("Успех", f"Код отправлен на номер: {phone}")

        # Кнопка отправки кода
        send_code_button = RoundedButton(
            frame,
            text="Отправить код по SMS",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            command=send_sms_code,
            width=200,
            height=30
        )
        send_code_button.place(relx=0.5, rely=0.82, anchor="center")

        # Кнопка "Гоу ходить"
        def validate_and_proceed():
            phone_number = phone_entry.get().strip()
            code = sms_entry.get().strip()
            if not phone_number:
                messagebox.showerror("Ошибка", "Введите номер телефона")
            elif not code:
                messagebox.showerror("Ошибка", "Введите код из SMS")
            elif code != "1515":
                messagebox.showerror("Ошибка", "Неверный код из SMS")
            else:
                self.show_frame("choose_a_situation")

        go_button = RoundedButton(
            frame,
            text="Гоу ходить",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            command=validate_and_proceed,
            width=350,
            height=45
        )
        go_button.place(relx=0.5, rely=0.9, anchor="center")

    def create_choose_a_situation_ui(self, frame):
        """Настройка UI выбора ситуаций"""
        if "choose_a_situation" in self.images:
            bg_label = Label(frame, image=self.images["choose_a_situation"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Кнопка настроек (шестерёнка)
        if "gear_icon" in self.images:
            gear_button = RoundedButton(
                frame,
                text="⚙️",
                bg="white",
                fg="black",
                active_bg="black",
                active_fg="white",
                radius=25,
                command=lambda: self.show_frame("settings"),
                width=20,
                height=30
            )
            gear_button.place(relx=0.1, rely=0.07, anchor="center")

        # Список ситуаций
        situations = [
            ("Проспал на работу", "Save_me_from_my_boss"),
            ("Горит дедлайн", "required_time"),
            ("Выход в субботу", "I_m_not_going_to_work_on_Saturday"),
            ("Гуляем с друзьями", "To_a_bar_with_friends"),
            ("Оставить отзыв", "Feedback_end")
        ]
        for i, (text, target) in enumerate(situations):
            RoundedButton(
                frame,
                text=text,
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                radius=25,
                command=lambda t=target: self.show_frame(t),
                width=300,
                height=50
            ).place(relx=0.5, rely=0.2 + i * 0.1, anchor="center")

        # Кнопка "Потерял телефон"
        RoundedButton(
            frame,
            text="Потерял телефон",
            bg="red",
            fg="white",
            active_bg="dark red",
            active_fg="black",
            radius=25,
            command=lambda: self.show_frame("Phone_loss"),
            width=300,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_save_me_from_my_boss_ui(self, frame):
        """Экран 'Проспал на работу'"""
        Label(frame, text="Проспал на работу", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_required_time_ui(self, frame):
        """Экран 'Горит дедлайн'"""
        Label(frame, text="Горит дедлайн", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_saturday_ui(self, frame):
        """Экран 'Выход в субботу'"""
        Label(frame, text="Выход в субботу", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_bar_ui(self, frame):
        """Экран 'Гуляем с друзьями'"""
        Label(frame, text="Гуляем с друзьями", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_feedback_ui(self, frame):
        """Экран 'Оставить отзыв'"""
        Label(frame, text="Оставить отзыв", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_phone_loss_ui(self, frame):
        """Экран 'Потерял телефон'"""
        Label(frame, text="Потерял телефон", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_settings_ui(self, frame):
        """Экран 'Настройки'"""
        Label(frame, text="Настройки", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")


if __name__ == "__main__":
    app = App()
    app.mainloop()