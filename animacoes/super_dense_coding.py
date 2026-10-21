from manim import *
import numpy as np


class SuperDenseCoding(Scene):
    def gate(self, label, x, y, color=BLUE):
        box = Square(side_length=0.46, color=color, fill_color=BLACK, fill_opacity=1)
        text = MathTex(label, font_size=28)
        return VGroup(box, text).move_to([x, y, 0])

    def cnot(self, x, top, bottom):
        line = Line([x, bottom, 0], [x, top, 0], color=BLUE)
        control = Dot([x, top, 0], radius=0.06, color=BLUE)
        target = Circle(radius=0.14, color=BLUE).move_to([x, bottom, 0])
        cross = VGroup(
            Line([x - 0.14, bottom, 0], [x + 0.14, bottom, 0], color=BLUE),
            Line([x, bottom - 0.14, 0], [x, bottom + 0.14, 0], color=BLUE),
        )
        return VGroup(line, control, target, cross)

    def qubit(self, name, color):
        circle = Circle(radius=0.25, color=color, fill_color=color, fill_opacity=0.25)
        letter = MathTex(name, font_size=28).move_to(circle)
        label = Text(f"qubit {name}", font_size=20).next_to(circle, DOWN, buff=0.14)
        return VGroup(circle, letter, label)

    def laboratory(self, name, x, color):
        box = RoundedRectangle(width=3.6, height=2.25, corner_radius=0.15, color=color)
        box.move_to([x, 0.45, 0])
        label = Text(name, font_size=30, color=color).move_to([x, 1.2, 0])
        return VGroup(box, label)

    def replace_text(self, current, replacement):
        return Succession(FadeOut(current), FadeIn(replacement), run_time=1)

    def output_probabilities(self, message):
        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        identity = np.eye(2)
        pauli_x = np.array([[0, 1], [1, 0]])
        pauli_z = np.diag([1, -1])
        cnot = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
        state = cnot @ np.kron(hadamard, identity) @ np.array([1, 0, 0, 0])
        if message[1] == "1":
            state = np.kron(pauli_x, identity) @ state
        if message[0] == "1":
            state = np.kron(pauli_z, identity) @ state
        state = np.kron(hadamard, identity) @ cnot @ state
        return np.abs(state) ** 2

    def construct(self):
        message = "10"
        title = Text("Super Dense Coding", font_size=40).to_edge(UP, buff=0.25)
        subtitle = Text("2 bits clássicos com o envio de 1 qubit e um par emaranhado compartilhado", font_size=22)
        subtitle.move_to(UP * 2.85)
        stage = Text("1. Preparar o par emaranhado", font_size=27).move_to(UP * 2.2)
        source = self.laboratory("Fonte de pares", 0, GRAY)
        alice_qubit = self.qubit("A", BLUE).move_to(LEFT * 0.65 + UP * 0.2)
        bob_qubit = self.qubit("B", TEAL).move_to(RIGHT * 0.65 + UP * 0.2)
        alice = self.laboratory("Alice", -3.9, BLUE)
        bob = self.laboratory("Bob", 3.9, TEAL)
        equation = MathTex(r"|00\rangle", font_size=34).move_to(DOWN * 1.2)

        top, bottom = -2.4, -3.05
        wires = VGroup(*[
            Line([-5.1, y, 0], [5.1, y, 0], color=GRAY, stroke_width=2)
            for y in [top, bottom]
        ])
        wire_labels = VGroup(
            MathTex(r"A:\ |0\rangle", font_size=23).move_to([-5.85, top, 0]),
            MathTex(r"B:\ |0\rangle", font_size=23).move_to([-5.85, bottom, 0]),
        )
        headings = VGroup(
            Text("Preparação", font_size=19).move_to([-3.9, -1.95, 0]),
            Text("Alice codifica", font_size=19).move_to([-1.2, -1.95, 0]),
            Text("Bob decodifica e mede", font_size=19).move_to([3.25, -1.95, 0]),
        )
        first_hadamard = self.gate("H", -4.4, top)
        first_cnot = self.cnot(-3.35, top, bottom)
        encoding = VGroup(
            self.gate("I", -1.65, top, YELLOW),
            self.gate("Z", -0.6, top, YELLOW),
        )
        last_cnot = self.cnot(1.75, top, bottom)
        last_hadamard = self.gate("H", 2.85, top)
        measurements = VGroup(self.gate("M", 4.15, top, GREEN), self.gate("M", 4.15, bottom, GREEN))
        gates = VGroup(first_hadamard, first_cnot, encoding, last_cnot, last_hadamard, measurements)
        gates.set_opacity(0.25)
        circuit = VGroup(wires, wire_labels, headings, gates)

        self.play(Write(title), FadeIn(subtitle))
        self.play(FadeIn(stage), FadeIn(source), FadeIn(alice_qubit), FadeIn(bob_qubit))
        self.play(FadeIn(circuit), Write(equation))
        next_equation = MathTex(r"\frac{|00\rangle+|10\rangle}{\sqrt{2}}", font_size=34).move_to(equation)
        self.play(first_hadamard.animate.set_opacity(1), self.replace_text(equation, next_equation))
        equation = next_equation
        next_equation = MathTex(r"|\Phi^+\rangle=\frac{|00\rangle+|11\rangle}{\sqrt{2}}", font_size=34).move_to(equation)
        self.play(first_cnot.animate.set_opacity(1), self.replace_text(equation, next_equation))
        equation = next_equation
        self.wait(1)

        next_stage = Text("Compartilhar: um qubit para cada participante", font_size=27).move_to(stage)
        self.play(self.replace_text(stage, next_stage), FadeOut(source))
        stage = next_stage
        self.play(
            FadeIn(alice), FadeIn(bob),
            alice_qubit.animate.move_to(LEFT * 3.9 + UP * 0.2),
            bob_qubit.animate.move_to(RIGHT * 3.9 + UP * 0.2),
            run_time=2,
        )
        link = DashedLine([-2.05, 0.4, 0], [2.05, 0.4, 0], color=YELLOW)
        link_label = Text("Par emaranhado", font_size=22, color=YELLOW).next_to(link, UP, buff=0.2)
        self.play(Create(link), Write(link_label))
        self.wait(1)

        next_stage = Text("2. Alice aplica Z ao qubit A e codifica 10", font_size=27).move_to(stage)
        message_label = Text(f"Mensagem: {message}", font_size=25, color=YELLOW).move_to([-3.9, -0.45, 0])
        self.play(self.replace_text(stage, next_stage), Write(message_label))
        stage = next_stage
        self.play(encoding.animate.set_opacity(1), Indicate(alice_qubit, color=YELLOW))
        next_equation = MathTex(r"|\Phi^-\rangle=\frac{|00\rangle-|11\rangle}{\sqrt{2}}", font_size=34).move_to(equation)
        self.play(self.replace_text(equation, next_equation))
        equation = next_equation
        self.wait(1.5)

        next_stage = Text("3. Alice envia somente o qubit A", font_size=27).move_to(stage)
        arrow = Arrow([-1.95, 0.85, 0], [1.95, 0.85, 0], color=YELLOW, buff=0)
        transmission = Text("1 qubit", font_size=23, color=YELLOW).next_to(arrow, UP, buff=0.18)
        self.play(self.replace_text(stage, next_stage), FadeOut(link), FadeOut(link_label))
        stage = next_stage
        self.play(Create(arrow), Write(transmission), bob_qubit.animate.move_to([4.65, 0.2, 0]))
        self.play(alice_qubit.animate.move_to([3.1, 0.2, 0]), run_time=2.5)
        self.wait(1)

        next_stage = Text("4. Bob aplica CNOT e Hadamard", font_size=27).move_to(stage)
        self.play(self.replace_text(stage, next_stage), FadeOut(arrow), FadeOut(transmission))
        stage = next_stage
        next_equation = MathTex(r"\frac{|00\rangle-|10\rangle}{\sqrt{2}}=|-\rangle|0\rangle", font_size=34).move_to(equation)
        self.play(last_cnot.animate.set_opacity(1), self.replace_text(equation, next_equation))
        equation = next_equation
        next_equation = MathTex(r"|10\rangle", font_size=34).move_to(equation)
        self.play(last_hadamard.animate.set_opacity(1), self.replace_text(equation, next_equation))
        equation = next_equation
        self.play(measurements.animate.set_opacity(1))
        received = format(int(np.argmax(self.output_probabilities(message))), "02b")
        received_label = Text(f"Recebido: {received}", font_size=23, color=GREEN).move_to([3.9, -0.45, 0])
        next_stage = Text(f"Bob recuperou {received} com 100% de probabilidade", font_size=27, color=GREEN).move_to(stage)
        self.play(self.replace_text(stage, next_stage), Write(received_label))
        stage = next_stage
        self.wait(2.5)

        content = VGroup(subtitle, stage, alice, bob, alice_qubit, bob_qubit, equation, circuit, message_label, received_label)
        self.play(FadeOut(content))
        self.show_messages()

    def show_messages(self):
        heading = Text("As quatro mensagens possíveis", font_size=30).move_to(UP * 2.55)
        positions = [-4.8, -2.3, 1.15, 4.7]
        headers = VGroup(*[
            Text(label, font_size=21).move_to([x, 1.65, 0])
            for x, label in zip(positions, ["Alice envia", "Alice aplica", "Estado compartilhado", "Bob recebe"])
        ])
        self.play(Write(heading), FadeIn(headers))
        descriptions = [
            ("00", "I", r"\frac{|00\rangle+|11\rangle}{\sqrt{2}}"),
            ("01", "X", r"\frac{|01\rangle+|10\rangle}{\sqrt{2}}"),
            ("10", "Z", r"\frac{|00\rangle-|11\rangle}{\sqrt{2}}"),
            ("11", r"X\ \to\ Z", r"\frac{|01\rangle-|10\rangle}{\sqrt{2}}"),
        ]
        for index, (message, operation, state) in enumerate(descriptions):
            y = 0.8 - index * 0.95
            probabilities = self.output_probabilities(message)
            received = format(int(np.argmax(probabilities)), "02b")
            row = VGroup(
                Text(message, font_size=30, color=YELLOW).move_to([positions[0], y, 0]),
                MathTex(operation, font_size=32).move_to([positions[1], y, 0]),
                MathTex(state, font_size=30).move_to([positions[2], y, 0]),
                Text(f"{received}  (100%)", font_size=26, color=GREEN).move_to([positions[3], y, 0]),
            )
            self.play(FadeIn(row, shift=UP * 0.1))
            self.wait(0.7)
        note = Text("Recurso necessário: um par emaranhado previamente compartilhado.", font_size=22)
        note.move_to(DOWN * 3.2)
        self.play(Write(note))
        self.wait(4)
