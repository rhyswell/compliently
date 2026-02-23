import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from pdf_parser import extract_text_from_pdf
from guideline_parser import GuidelineParser
from rule_engine import RuleEngine
from semantic_engine import SemanticEngine
from scoring import ScoringEngine


class CompliantlyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Compliantly - AI Brand Compliance Checker")
        self.root.geometry("1000x700")

        self.guidelines_text = ""
        self._build_ui()

        # Engines
        self.guideline_parser = GuidelineParser()
        self.rule_engine = RuleEngine()
        self.semantic_engine = SemanticEngine()
        self.scoring_engine = ScoringEngine()

    def _build_ui(self):
        # Frames
        left_frame = tk.Frame(self.root)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self.root)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # Guidelines section
        tk.Label(left_frame, text="Brand Guidelines").pack()
        self.guidelines_box = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD)
        self.guidelines_box.pack(fill="both", expand=True)

        tk.Button(
            left_frame,
            text="Upload PDF",
            command=self._upload_pdf,
        ).pack(pady=5)

        # Content section
        tk.Label(right_frame, text="Content to Evaluate").pack()
        self.content_box = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD)
        self.content_box.pack(fill="both", expand=True)

        # Run button
        tk.Button(
            bottom_frame,
            text="Run Compliance Check",
            command=self._run_compliance,
            height=2,
        ).pack(fill="x")

        # Results
        tk.Label(bottom_frame, text="Results").pack(pady=(10, 0))
        self.results_box = scrolledtext.ScrolledText(
            bottom_frame, wrap=tk.WORD, height=12
        )
        self.results_box.pack(fill="both", expand=True)

    def _upload_pdf(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return

        try:
            text = extract_text_from_pdf(file_path)
            self.guidelines_box.delete("1.0", tk.END)
            self.guidelines_box.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF:\n{str(e)}")

    def _run_compliance(self):
        try:
            guidelines_raw = self.guidelines_box.get("1.0", tk.END).strip()
            content = self.content_box.get("1.0", tk.END).strip()

            if not guidelines_raw or not content:
                messagebox.showwarning(
                    "Missing Input",
                    "Both guidelines and content are required.",
                )
                return

            # 1. Parse guidelines (GPT)
            structured_guidelines = self.guideline_parser.parse(
                guidelines_raw
            )

            # 2. Deterministic rule engine
            deterministic_score, deterministic_violations = (
                self.rule_engine.evaluate(
                    structured_guidelines,
                    content,
                )
            )

            # 3. Semantic engine (GPT)
            semantic_evaluation = self.semantic_engine.evaluate(
                structured_guidelines,
                content,
            )

            # 4. Aggregate scoring
            report = self.scoring_engine.aggregate(
                deterministic_score,
                deterministic_violations,
                semantic_evaluation,
            )

            self._display_results(report)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _display_results(self, report):
        self.results_box.delete("1.0", tk.END)

        output = (
            f"Overall Score: {report.overall_score}\n"
            f"Deterministic Score: {report.deterministic_score}\n"
            f"Semantic Score: {report.semantic_score}\n"
            f"Confidence: {report.confidence}\n\n"
            "Deterministic Violations:\n"
        )

        for v in report.deterministic_violations:
            output += f"- [{v.severity.upper()}] {v.message}\n"

        output += "\nSemantic Violations:\n"
        for v in report.semantic_violations:
            output += (
                f"- {v.type}: {v.explanation}\n"
                f"  Suggestion: {v.suggestion}\n"
            )

        output += "\nSuggested Rewrite:\n"
        output += report.rewrite

        self.results_box.insert(tk.END, output)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompliantlyApp(root)
    root.mainloop()
