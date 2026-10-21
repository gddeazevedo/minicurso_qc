from manim import *
import numpy as np


class DeutschJozsaAlgorithm(Scene):
    def construct(self):
        title = Text("Algoritmo de Deutsch–Jozsa", font_size=38)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))

        self.show_case(False)
        self.show_case(True)

        heading = Text("Uma consulta ao oráculo", font_size=30)
        heading.move_to(UP * 2)
        constant = VGroup(
            Text("Identidade: constante", font_size=26, color=GREEN),
            MathTex(r"P(000)=1", font_size=34),
        ).arrange(DOWN, buff=0.4).move_to(LEFT * 3 + UP * 0.4)
        balanced = VGroup(
            Text("Paridade: balanceada", font_size=26, color=BLUE),
            MathTex(r"P(111)=1,\qquad P(000)=0", font_size=30),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3 + UP * 0.4)
        note = Text("O qubit auxiliar não é medido.", font_size=25)
        note.move_to(DOWN * 1.3)
        self.play(FadeIn(heading), FadeIn(constant), FadeIn(balanced))
        self.play(Write(note))
        self.wait(4)

    def gate(self, label, x, y, color=BLUE):
        box = Square(side_length=0.43, color=color, fill_color=BLACK, fill_opacity=1)
        text = MathTex(label, font_size=26)
        return VGroup(box, text).move_to([x, y, 0])

    def replace_text(self, current, replacement):
        return Succession(FadeOut(current), FadeIn(replacement), run_time=1)

    def cnot(self, x, control_y, target_y):
        line = Line([x, target_y, 0], [x, control_y, 0], color=BLUE)
        control = Dot([x, control_y, 0], radius=0.06, color=BLUE)
        target = Circle(radius=0.13, color=BLUE).move_to([x, target_y, 0])
        cross = VGroup(
            Line([x - 0.13, target_y, 0], [x + 0.13, target_y, 0], color=BLUE),
            Line([x, target_y - 0.13, 0], [x, target_y + 0.13, 0], color=BLUE),
        )
        return VGroup(line, control, target, cross)

    def probability_bars(self, axes, probabilities, phases=None):
        bars = VGroup()
        for index, probability in enumerate(probabilities):
            height = max(float(probability) * 1.35, 0.006)
            color = YELLOW if phases is not None and phases[index] < 0 else BLUE
            bar = Rectangle(
                width=0.65,
                height=height,
                color=color,
                fill_color=color,
                fill_opacity=0.85,
                stroke_width=1,
            )
            bar.move_to(axes.c2p(index, 0) + UP * height / 2)
            bars.add(bar)
        return bars

    def show_case(self, balanced):
        case_name = "Balanceada: paridade dos três bits" if balanced else "Constante: identidade, f(x) = 0"
        case_title = Text(case_name, font_size=28, color=BLUE if balanced else GREEN)
        case_title.move_to(UP * 2.85)
        stage = Text("1. Preparar o qubit auxiliar", font_size=25)
        stage.move_to(UP * 2.22)

        positions = [1.45, 0.88, 0.31, -0.26]
        wires = VGroup(*[
            Line([-5.35, y, 0], [5.15, y, 0], stroke_width=2, color=GRAY)
            for y in positions
        ])
        labels = VGroup(*[
            MathTex(rf"q_{{{index}}}:\ |0\rangle", font_size=23).move_to([-6.05, y, 0])
            for index, y in enumerate(positions)
        ])
        auxiliary = Text("auxiliar", font_size=17, color=GRAY)
        auxiliary.next_to(labels[-1], DOWN, buff=0.1)
        preparation = self.gate("X", -4.7, positions[-1])
        first_hadamards = VGroup(*[self.gate("H", -3.55, y) for y in positions])
        last_hadamards = VGroup(*[self.gate("H", 2.8, y) for y in positions[:3]])
        measurements = VGroup(*[self.gate("M", 4.3, y, GREEN) for y in positions[:3]])
        if balanced:
            oracle = VGroup(*[
                self.cnot(x, positions[index], positions[-1])
                for index, x in enumerate([-1.5, -0.25, 1])
            ])
        else:
            oracle = VGroup(self.gate("I", -0.25, positions[-1], GREEN))
        oracle_label = MathTex(r"U_f", font_size=23).move_to([-0.25, 1.91, 0])
        gates = VGroup(preparation, first_hadamards, oracle, last_hadamards, measurements)
        gates.set_opacity(0.3)
        equation = MathTex(r"|0\rangle_{\rm aux}\ \xrightarrow{X}\ |1\rangle_{\rm aux}", font_size=28)
        equation.move_to(DOWN * 0.95)

        axes = Axes(
            x_range=[-0.5, 7.5, 1],
            y_range=[0, 1, 0.5],
            x_length=10,
            y_length=1.35,
            tips=False,
            axis_config={"include_ticks": False, "stroke_width": 1},
        )
        axes.move_to(DOWN * 2.45)
        state_labels = VGroup(*[
            Text(format(index, "03b"), font_size=20).next_to(axes.c2p(index, 0), DOWN, buff=0.12)
            for index in range(8)
        ])
        chart_title = Text("Probabilidade de medir as entradas", font_size=20)
        chart_title.move_to([-1.3, -1.5, 0])
        chart_scale = VGroup(
            Text("1", font_size=18).next_to(axes.c2p(-0.5, 1), LEFT, buff=0.12),
            Text("0", font_size=18).next_to(axes.c2p(-0.5, 0), LEFT, buff=0.12),
        )

        self.play(FadeIn(case_title), FadeIn(stage), Create(wires), Write(labels), FadeIn(auxiliary))
        self.play(FadeIn(gates), FadeIn(oracle_label))
        self.play(preparation.animate.set_opacity(1), Write(equation))
        self.play(Indicate(preparation, color=YELLOW))
        self.wait(1)

        hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        transform = np.kron(np.kron(hadamard, hadamard), hadamard)
        state = transform[:, 0]
        bars = self.probability_bars(axes, np.abs(state) ** 2)
        next_stage = Text("2. Criar a superposição", font_size=25).move_to(stage)
        next_equation = MathTex(r"|+\rangle^{\otimes 3}\,|-\rangle_{\rm aux}", font_size=30).move_to(equation)
        self.play(self.replace_text(stage, next_stage), first_hadamards.animate.set_opacity(1), self.replace_text(equation, next_equation))
        stage, equation = next_stage, next_equation
        self.play(Create(axes), Write(state_labels), FadeIn(chart_scale), FadeIn(chart_title), FadeIn(bars))
        self.wait(1.5)

        phases = np.array([(-1) ** format(index, "03b").count("1") for index in range(8)]) if balanced else np.ones(8)
        next_stage = Text("3. Consultar o oráculo uma vez", font_size=25).move_to(stage)
        oracle_formula = r"(-1)^{x_0\oplus x_1\oplus x_2}|x\rangle\,|-\rangle" if balanced else r"I|x\rangle\,|-\rangle=|x\rangle\,|-\rangle"
        next_equation = MathTex(oracle_formula, font_size=29).move_to(equation)
        legend = Text("Azul: fase +    Amarelo: fase −", font_size=18)
        legend.move_to([3.4, -1.5, 0])
        self.play(self.replace_text(stage, next_stage), oracle.animate.set_opacity(1))
        stage = next_stage
        self.play(Indicate(oracle, color=YELLOW), self.replace_text(equation, next_equation))
        equation = next_equation
        state = phases * state
        self.play(Transform(bars, self.probability_bars(axes, np.abs(state) ** 2, phases)), FadeIn(legend))
        self.wait(2)

        next_stage = Text("4. Aplicar Hadamard nas entradas e medir", font_size=25).move_to(stage)
        final_state = "111" if balanced else "000"
        next_equation = MathTex(rf"|{final_state}\rangle\,|-\rangle_{{\rm aux}}", font_size=30).move_to(equation)
        self.play(self.replace_text(stage, next_stage), last_hadamards.animate.set_opacity(1))
        stage = next_stage
        self.play(Indicate(last_hadamards, color=YELLOW))
        state = transform @ state
        probabilities = np.abs(state) ** 2
        self.play(self.replace_text(equation, next_equation), Transform(bars, self.probability_bars(axes, probabilities)), FadeOut(legend))
        equation = next_equation
        self.play(measurements.animate.set_opacity(1))
        result = Text(f"Resultado: {final_state}  →  {'BALANCEADA' if balanced else 'CONSTANTE'}", font_size=27, color=GREEN)
        result.move_to(stage)
        self.play(self.replace_text(stage, result), Indicate(bars[int(np.argmax(probabilities))], color=GREEN))
        stage = result
        self.wait(2.5)

        content = VGroup(case_title, stage, wires, labels, auxiliary, gates, oracle_label, equation, axes, state_labels, chart_scale, chart_title, bars)
        self.play(FadeOut(content))
