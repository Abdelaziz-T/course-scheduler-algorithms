"""
Online Course Scheduler — Tkinter GUI
Student Project | Algorithms: Conflict Check, Filter, Greedy, Backtracking

"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

# ─────────────────────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────────────────────

COURSES = [
    {"name": "Math 101",       "day": "Sun", "start":  8, "end": 10, "seats": 30},
    {"name": "CS 101",         "day": "Sun", "start": 10, "end": 12, "seats": 25},
    {"name": "Physics",        "day": "Sun", "start": 13, "end": 15, "seats": 20},
    {"name": "English",        "day": "Mon", "start":  8, "end": 10, "seats": 40},
    {"name": "Chemistry",      "day": "Mon", "start": 10, "end": 12, "seats": 18},
    {"name": "History",        "day": "Mon", "start": 13, "end": 15, "seats": 35},
    {"name": "Statistics",     "day": "Tue", "start":  8, "end": 10, "seats": 22},
    {"name": "Networks",       "day": "Tue", "start": 10, "end": 12, "seats": 28},
    {"name": "Databases",      "day": "Tue", "start": 14, "end": 16, "seats": 24},
    {"name": "Algorithms",     "day": "Wed", "start":  9, "end": 11, "seats": 20},
    {"name": "OS Concepts",    "day": "Wed", "start": 11, "end": 13, "seats": 22},
    {"name": "Calculus",       "day": "Wed", "start": 14, "end": 16, "seats": 30},
    {"name": "Data Science",   "day": "Thu", "start":  8, "end": 10, "seats": 25},
    {"name": "AI Basics",      "day": "Thu", "start": 10, "end": 12, "seats": 20},
    {"name": "Web Dev",        "day": "Thu", "start": 13, "end": 15, "seats": 35},
    {"name": "Cyber Security", "day": "Sat", "start":  9, "end": 11, "seats": 15},
    {"name": "Linear Algebra", "day": "Sat", "start": 11, "end": 13, "seats": 28},
    {"name": "Discrete Math",  "day": "Sat", "start": 14, "end": 16, "seats": 22},
]

DAYS_ORDER = ["Sun", "Mon", "Tue", "Wed", "Thu", "Sat"]

# ─────────────────────────────────────────────────────────────
#  ALGORITHMS (implemented from scratch — no built-in solvers)
# ─────────────────────────────────────────────────────────────

def has_conflict(c1, c2):
    """O(1) — same day + overlapping times"""
    if c1["day"] != c2["day"]:
        return False
    return c1["start"] < c2["end"] and c2["start"] < c1["end"]


def filter_by_preference(courses, preferred_days, time_pref):
    """O(n) — keep only courses matching student preferences"""
    result = []
    for course in courses:
        if preferred_days and course["day"] not in preferred_days:
            continue
        if time_pref == "Morning" and course["start"] >= 12:
            continue
        if time_pref == "Afternoon" and course["start"] < 12:
            continue
        result.append(course)
    return result


def greedy_schedule(courses):
    """O(n²) — add course if no conflict with already scheduled"""
    schedule = []
    for course in courses:
        if all(not has_conflict(course, s) for s in schedule):
            schedule.append(course)
    return schedule


def backtrack(courses, schedule, index):
    """O(2ⁿ) — True exhaustive search to find the MAXIMUM possible schedule"""
    # Base Case: لو وصلنا لآخر القائمة، نرجع بنسخة من الجدول الحالي
    if index == len(courses): 
        return list(schedule)
    
    res_skip = backtrack(courses, schedule, index + 1)
    
    res_take = None
    course = courses[index]
    
    if all(not has_conflict(course, s) for s in schedule):
        schedule.append(course)  # نأخذ الكورس
        res_take = backtrack(courses, schedule, index + 1) # ندخل في التفريعة
        schedule.pop()           # التراجع الفعلي (Backtrack) عشان نفضي المكان للاحتمالات التانية
        
    # ── المقارنة والقرار: مين في الطريقين طلعلي عدد كورسات أكتر؟ ──
    if res_take and len(res_take) > len(res_skip):
        return res_take  # طريق أخذ الكورس طلع أفضل
    
    return res_skip      # طريق تخطي الكورس طلع أفضل أو متساوي


def generate_random_courses(n):
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Sat"]
    starts = [8, 9, 10, 11, 12, 13, 14]
    out = []
    for i in range(n):
        s = random.choice(starts)
        out.append({
            "name": f"Course_{i}",
            "day": random.choice(days),
            "start": s,
            "end": s + 2,
            "seats": 20,
        })
    return out


# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def fmt_time(h):
    if h == 0:   return "12:00 AM"
    if h < 12:   return f"{h}:00 AM"
    if h == 12:  return "12:00 PM"
    return f"{h-12}:00 PM"


# ─────────────────────────────────────────────────────────────
#  THEME
# ─────────────────────────────────────────────────────────────

BG        = "#0f1117"
SURFACE   = "#1a1d27"
SURFACE2  = "#22263a"
ACCENT    = "#4f8ef7"
ACCENT2   = "#7c5cbf"
SUCCESS   = "#3dd68c"
WARNING   = "#f5a623"
DANGER    = "#f05252"
TEXT      = "#e8eaf0"
TEXT2     = "#8b92a8"
BORDER    = "#2d3250"

FONT_H1   = ("Georgia", 20, "bold")
FONT_H2   = ("Georgia", 14, "bold")
FONT_H3   = ("Helvetica", 11, "bold")
FONT_BODY = ("Helvetica", 10)
FONT_MONO = ("Courier", 10)
FONT_SMALL= ("Helvetica", 9)


# ─────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────

class CourseSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Scheduler")
        self.geometry("980x680")
        self.minsize(860, 580)
        self.configure(bg=BG)
        self.resizable(True, True)

        # style ttk
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",        background=BG,      borderwidth=0)
        style.configure("TNotebook.Tab",    background=SURFACE, foreground=TEXT2,
                        padding=[16, 8],    font=FONT_H3,       borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", SURFACE2)],
                  foreground=[("selected", TEXT)])
        style.configure("Treeview",         background=SURFACE, foreground=TEXT,
                        fieldbackground=SURFACE, rowheight=28,  font=FONT_BODY,
                        borderwidth=0)
        style.configure("Treeview.Heading", background=SURFACE2, foreground=ACCENT,
                        font=FONT_H3,       borderwidth=0)
        style.map("Treeview", background=[("selected", ACCENT2)])
        style.configure("TScrollbar",       background=SURFACE2, troughcolor=SURFACE,
                        borderwidth=0,      arrowcolor=TEXT2)

        self._build_header()
        self._build_notebook()

    # ── Header ──────────────────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self, bg=SURFACE, height=64)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="◈  Course Scheduler", font=FONT_H1,
                 bg=SURFACE, fg=TEXT).pack(side="left", padx=24, pady=14)

        tk.Label(hdr, text="Algorithms: Conflict Check · Filter · Greedy · Backtracking",
                 font=FONT_SMALL, bg=SURFACE, fg=TEXT2).pack(side="right", padx=24)

    # ── Notebook tabs ────────────────────────────────────────

    def _build_notebook(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab_scheduler  = tk.Frame(self.nb, bg=BG)
        self.tab_courses    = tk.Frame(self.nb, bg=BG)
        self.tab_analysis   = tk.Frame(self.nb, bg=BG)

        self.nb.add(self.tab_scheduler, text="  Build Schedule  ")
        self.nb.add(self.tab_courses,   text="  All Courses  ")
        self.nb.add(self.tab_analysis,  text="  Algorithm Analysis  ")

        self._build_scheduler_tab()
        self._build_courses_tab()
        self._build_analysis_tab()

    # ─────────────────────────────────────────────────────────
    #  TAB 1 — BUILD SCHEDULE
    # ─────────────────────────────────────────────────────────

    def _build_scheduler_tab(self):
        tab = self.tab_scheduler
        # left panel: preferences
        left = tk.Frame(tab, bg=SURFACE, width=280)
        left.pack(side="left", fill="y", padx=(16,8), pady=16)
        left.pack_propagate(False)

        # right panel: results
        right = tk.Frame(tab, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(0,16), pady=16)

        # ── Preferences Panel ──
        tk.Label(left, text="Preferences", font=FONT_H2,
                 bg=SURFACE, fg=TEXT).pack(anchor="w", padx=16, pady=(16,4))
        tk.Label(left, text="Customize your schedule below",
                 font=FONT_SMALL, bg=SURFACE, fg=TEXT2).pack(anchor="w", padx=16, pady=(0,14))

        self._section(left, "Preferred Days")
        self.day_vars = {}
        day_frame = tk.Frame(left, bg=SURFACE)
        day_frame.pack(fill="x", padx=16, pady=(0,12))
        for i, d in enumerate(DAYS_ORDER):
            v = tk.BooleanVar(value=True)
            self.day_vars[d] = v
            cb = tk.Checkbutton(day_frame, text=d, variable=v,
                                bg=SURFACE, fg=TEXT, selectcolor=SURFACE2,
                                activebackground=SURFACE, activeforeground=TEXT,
                                font=FONT_BODY, cursor="hand2")
            cb.grid(row=i//3, column=i%3, sticky="w", padx=4, pady=2)

        self._section(left, "Time of Day")
        self.time_pref = tk.StringVar(value="Any")
        for opt in ["Any", "Morning", "Afternoon"]:
            rb = tk.Radiobutton(left, text=opt, variable=self.time_pref, value=opt,
                                bg=SURFACE, fg=TEXT, selectcolor=SURFACE2,
                                activebackground=SURFACE, font=FONT_BODY, cursor="hand2")
            rb.pack(anchor="w", padx=20, pady=1)

        self._section(left, "Algorithm")
        self.algo_var = tk.StringVar(value="Greedy")
        for opt, desc in [("Greedy","O(n²) — Fast"), ("Backtracking","O(2ⁿ) — Thorough")]:
            f = tk.Frame(left, bg=SURFACE)
            f.pack(fill="x", padx=16, pady=2)
            tk.Radiobutton(f, text=opt, variable=self.algo_var, value=opt,
                           bg=SURFACE, fg=TEXT, selectcolor=SURFACE2,
                           activebackground=SURFACE, font=FONT_BODY, cursor="hand2").pack(side="left")
            tk.Label(f, text=desc, font=FONT_SMALL, bg=SURFACE, fg=TEXT2).pack(side="left", padx=6)

        # spacer
        tk.Frame(left, bg=SURFACE).pack(fill="both", expand=True)

        # generate button
        btn = tk.Button(left, text="Generate Schedule ▶",
                        font=FONT_H3, bg=ACCENT, fg="white",
                        activebackground="#3a7ae0", activeforeground="white",
                        relief="flat", cursor="hand2", pady=10,
                        command=self._generate_schedule)
        btn.pack(fill="x", padx=16, pady=16)

        # ── Results Panel ──
        tk.Label(right, text="Your Schedule", font=FONT_H2,
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(4,2))
        tk.Label(right, text="Generated schedule will appear here",
                 font=FONT_SMALL, bg=BG, fg=TEXT2).pack(anchor="w", pady=(0,10))

        # status bar
        self.status_var = tk.StringVar(value="Select preferences and click Generate")
        status_bar = tk.Frame(right, bg=SURFACE2, pady=6)
        status_bar.pack(fill="x", pady=(0,8))
        self.status_lbl = tk.Label(status_bar, textvariable=self.status_var,
                                   font=FONT_BODY, bg=SURFACE2, fg=ACCENT)
        self.status_lbl.pack(side="left", padx=12)
        self.count_lbl = tk.Label(status_bar, text="",
                                  font=FONT_BODY, bg=SURFACE2, fg=SUCCESS)
        self.count_lbl.pack(side="right", padx=12)

        # result treeview
        cols = ("Course", "Day", "Time", "Seats")
        self.result_tree = ttk.Treeview(right, columns=cols, show="headings",
                                        selectmode="browse")
        for col, w in zip(cols, [200, 70, 160, 60]):
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=w, anchor="w")

        vsb = ttk.Scrollbar(right, orient="vertical", command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=vsb.set)
        self.result_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        # row tags
        self.result_tree.tag_configure("day_header", background=SURFACE2,
                                       foreground=ACCENT, font=FONT_H3)
        self.result_tree.tag_configure("course_row", background=SURFACE,
                                       foreground=TEXT)
        self.result_tree.tag_configure("conflict",   background="#3a1a1a",
                                       foreground=DANGER)

    def _section(self, parent, title):
        tk.Label(parent, text=title.upper(), font=("Helvetica", 9, "bold"),
                 bg=SURFACE, fg=ACCENT).pack(anchor="w", padx=16, pady=(12,4))

    def _generate_schedule(self):
        # collect preferences
        preferred_days = [d for d, v in self.day_vars.items() if v.get()]
        time_pref = self.time_pref.get()
        algo = self.algo_var.get()

        if not preferred_days:
            messagebox.showwarning("No days selected", "Please select at least one day.")
            return

        # filter
        filtered = filter_by_preference(COURSES, preferred_days, time_pref)
        if not filtered:
            self.status_var.set("No courses match your preferences.")
            self.count_lbl.config(text="")
            return

        # run algorithm
        t0 = time.time()
        if algo == "Backtracking":
            schedule = backtrack(filtered, [], 0) or []
        else:
            schedule = greedy_schedule(filtered)
        elapsed = (time.time() - t0) * 1000

        # sort by day then time
        schedule.sort(key=lambda c: (DAYS_ORDER.index(c["day"]), c["start"]))

        # populate tree
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

        current_day = None
        for c in schedule:
            if c["day"] != current_day:
                current_day = c["day"]
                self.result_tree.insert("", "end",
                    values=(f"── {current_day} ──", "", "", ""),
                    tags=("day_header",))
            self.result_tree.insert("", "end",
                values=(c["name"], c["day"],
                        f"{fmt_time(c['start'])} – {fmt_time(c['end'])}",
                        c["seats"]),
                tags=("course_row",))

        self.status_var.set(f"{algo} · {elapsed:.2f}ms · {len(filtered)} courses filtered")
        self.count_lbl.config(text=f"✔ {len(schedule)} scheduled")

    # ─────────────────────────────────────────────────────────
    #  TAB 2 — ALL COURSES
    # ─────────────────────────────────────────────────────────

    def _build_courses_tab(self):
        tab = self.tab_courses

        tk.Label(tab, text="All Available Courses", font=FONT_H2,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=16, pady=(16,2))
        tk.Label(tab, text=f"{len(COURSES)} courses loaded",
                 font=FONT_SMALL, bg=BG, fg=TEXT2).pack(anchor="w", padx=16, pady=(0,10))

        # search bar
        sf = tk.Frame(tab, bg=BG)
        sf.pack(fill="x", padx=16, pady=(0,8))
        tk.Label(sf, text="Search:", font=FONT_BODY, bg=BG, fg=TEXT2).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *_: self._filter_courses_table())
        se = tk.Entry(sf, textvariable=self.search_var, font=FONT_BODY,
                      bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
                      relief="flat", width=24)
        se.pack(side="left", padx=8, ipady=4)

        # day filter buttons
        self.day_filter = tk.StringVar(value="All")
        for d in ["All"] + DAYS_ORDER:
            tk.Radiobutton(sf, text=d, variable=self.day_filter, value=d,
                           bg=BG, fg=TEXT2, selectcolor=SURFACE2,
                           activebackground=BG, font=FONT_SMALL, cursor="hand2",
                           command=self._filter_courses_table).pack(side="left", padx=3)

        # table
        frame = tk.Frame(tab, bg=BG)
        frame.pack(fill="both", expand=True, padx=16, pady=(0,16))

        cols = ("Course", "Day", "Start", "End", "Duration", "Seats")
        self.courses_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for col, w in zip(cols, [180, 60, 100, 100, 90, 60]):
            self.courses_tree.heading(col, text=col)
            self.courses_tree.column(col, width=w, anchor="w")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.courses_tree.yview)
        self.courses_tree.configure(yscrollcommand=vsb.set)
        self.courses_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        # alternating row colors
        self.courses_tree.tag_configure("odd",  background=SURFACE)
        self.courses_tree.tag_configure("even", background=SURFACE2)

        self._populate_courses_table(COURSES)

    def _populate_courses_table(self, courses):
        for row in self.courses_tree.get_children():
            self.courses_tree.delete(row)
        for i, c in enumerate(courses):
            tag = "odd" if i % 2 == 0 else "even"
            dur = c["end"] - c["start"]
            self.courses_tree.insert("", "end", values=(
                c["name"], c["day"],
                fmt_time(c["start"]), fmt_time(c["end"]),
                f"{dur} hr{'s' if dur>1 else ''}",
                c["seats"]
            ), tags=(tag,))

    def _filter_courses_table(self):
        q = self.search_var.get().lower()
        day = self.day_filter.get()
        filtered = [c for c in COURSES
                    if (q in c["name"].lower() or q in c["day"].lower())
                    and (day == "All" or c["day"] == day)]
        self._populate_courses_table(filtered)

    # ─────────────────────────────────────────────────────────
    #  TAB 3 — ALGORITHM ANALYSIS
    # ─────────────────────────────────────────────────────────

    def _build_analysis_tab(self):
        tab = self.tab_analysis

        tk.Label(tab, text="Algorithm Analysis", font=FONT_H2,
                 bg=BG, fg=TEXT).pack(anchor="w", padx=16, pady=(16,2))
        tk.Label(tab, text="Empirical runtime comparison — Greedy O(n²) vs Backtracking O(2ⁿ)",
                 font=FONT_SMALL, bg=BG, fg=TEXT2).pack(anchor="w", padx=16, pady=(0,12))

        # controls
        cf = tk.Frame(tab, bg=BG)
        cf.pack(fill="x", padx=16, pady=(0,12))
        tk.Button(cf, text="▶  Run Benchmark", font=FONT_H3,
                  bg=ACCENT, fg="white", relief="flat", cursor="hand2",
                  activebackground="#3a7ae0", padx=16, pady=6,
                  command=self._run_analysis).pack(side="left")
        tk.Label(cf, text="Tests on n = 10, 20, 50, 100, 200 random courses",
                 font=FONT_SMALL, bg=BG, fg=TEXT2).pack(side="left", padx=16)

        # split: table left, big-O info right
        content = tk.Frame(tab, bg=BG)
        content.pack(fill="both", expand=True, padx=16, pady=(0,16))

        # results table
        left = tk.Frame(content, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        cols = ("n (courses)", "Greedy (ms)", "Backtrack (ms)", "Winner")
        self.analysis_tree = ttk.Treeview(left, columns=cols, show="headings", height=8)
        for col, w in zip(cols, [120, 130, 150, 100]):
            self.analysis_tree.heading(col, text=col)
            self.analysis_tree.column(col, width=w, anchor="center")
        self.analysis_tree.tag_configure("greedy_wins",  foreground=SUCCESS)
        self.analysis_tree.tag_configure("bt_wins",      foreground=WARNING)
        self.analysis_tree.tag_configure("too_slow",     foreground=DANGER)
        self.analysis_tree.pack(fill="both", expand=True)

        # Big-O summary cards
        right = tk.Frame(content, bg=BG, width=260)
        right.pack(side="left", fill="y", padx=(16,0))
        right.pack_propagate(False)

        self._algo_card(right, "Greedy Scheduler", "O(n²)",
            "For each course, check against all\nalready-scheduled courses.\nFast for large inputs.",
            ACCENT, SUCCESS)

        self._algo_card(right, "Backtracking Search", "O(2ⁿ)",
            "Tries every combination.\nBacktracks when conflict found.\nExpensive for large n.",
            ACCENT2, WARNING)

        self._algo_card(right, "Conflict Checker", "O(1)",
            "Compare two courses:\nsame day + overlapping times.\nUsed inside both algorithms.",
            "#3dd68c", SUCCESS)

        self._algo_card(right, "Preference Filter", "O(n)",
            "Loop once through all courses.\nKeep matching day and time.\nRuns before scheduling.",
            TEXT2, TEXT2)

        # log output
        tk.Label(tab, text="Output Log", font=FONT_H3,
                 bg=BG, fg=TEXT2).pack(anchor="w", padx=16)
        self.log_text = tk.Text(tab, height=7, font=FONT_MONO,
                                bg=SURFACE, fg=TEXT, insertbackground=TEXT,
                                relief="flat", state="disabled")
        self.log_text.pack(fill="x", padx=16, pady=(4,16))

    def _algo_card(self, parent, name, complexity, desc, accent_color, comp_color):
        card = tk.Frame(parent, bg=SURFACE, pady=10, padx=12)
        card.pack(fill="x", pady=6)
        tk.Label(card, text=name, font=FONT_H3, bg=SURFACE, fg=TEXT).pack(anchor="w")
        tk.Label(card, text=complexity, font=("Courier", 14, "bold"),
                 bg=SURFACE, fg=comp_color).pack(anchor="w")
        tk.Label(card, text=desc, font=FONT_SMALL, bg=SURFACE, fg=TEXT2,
                 justify="left").pack(anchor="w", pady=(4,0))

    def _run_analysis(self):
        # تنظيف الجدول والـ Log
        for row in self.analysis_tree.get_children():
            self.analysis_tree.delete(row)

        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", "Running benchmark...\n")
        self.log_text.config(state="disabled")
        self.update()

        sizes = [10, 20, 50, 100, 200]
        log_lines = []

        for n in sizes:
            data = generate_random_courses(n)

            # قياس وقت الـ Greedy (دايماً طيارة وسريع)
            t0 = time.time()
            greedy_schedule(data)
            g_ms = (time.time() - t0) * 1000

            # هنا التعديل السحري لحماية البرنامج
            if n <= 20: 
                t0 = time.time()
                backtrack(data, [], 0)
                bt_ms = (time.time() - t0) * 1000
                bt_str = f"{bt_ms:.3f}"
                winner = "Greedy" if g_ms <= bt_ms else "Backtrack"
                tag = "greedy_wins" if winner == "Greedy" else "bt_wins"
                log_lines.append(f"n={n:>3}  Greedy={g_ms:.3f}ms  Backtrack={bt_ms:.3f}ms  → {winner}")
            else:
                # أي n أكبر من 20 مش هنشغل الـ Backtracking عشان الجهاز ميهنجش
                bt_str = "too slow"
                winner = "Greedy"
                tag = "too_slow"
                log_lines.append(f"n={n:>3}  Greedy={g_ms:.3f}ms  Backtrack=N/A (2^n too slow)")

            self.analysis_tree.insert("", "end",
                values=(n, f"{g_ms:.3f}", bt_str, winner),
                tags=(tag,))
            self.update()

        log_lines.append("\nConclusion: Greedy is practical for large inputs.")
        log_lines.append("Backtracking is exhaustive but only feasible for small n (<=20).")

        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("end", "\n".join(log_lines))
        self.log_text.config(state="disabled")


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = CourseSchedulerApp()
    app.mainloop()
