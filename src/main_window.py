import tkinter as tk
from tkinter import ttk, messagebox
from calculator import FaktorialCalculator
from database import HistoryDatabase

class FaktorialApp:
    def __init__(self):
        # Setup window
        self.root = tk.Tk()
        self.root.title("Kalkulator Faktorial")
        self.root.geometry("900x650")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(True, True)
        
        # Style configuration
        self.setup_styles()
        
        # Initialize database
        self.db = HistoryDatabase()
        
        # Setup GUI
        self.setup_gui()
        
        # Load initial data
        self.update_history_display()
        self.update_statistics()
    
    def setup_styles(self):
        """Setup style untuk aplikasi"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#00cc66"
        self.secondary_color = "#3c3c3c"
        self.hover_color = "#4a4a4a"
        
        # Configure styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10), padding=10)
        self.style.configure("Accent.TButton", background=self.accent_color, foreground="white")
        self.style.configure("Danger.TButton", background="#ff4444", foreground="white")
        self.style.configure("TEntry", font=("Arial", 12), padding=8)
        self.style.configure("Treeview", background=self.secondary_color, fieldbackground=self.secondary_color, foreground=self.fg_color)
        self.style.configure("Treeview.Heading", background="#404040", foreground=self.fg_color)
        self.style.configure("TNotebook", background=self.bg_color)
        self.style.configure("TNotebook.Tab", background="#404040", foreground=self.fg_color, padding=[20, 10])
    
    def setup_gui(self):
        """Setup antarmuka grafis"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🧮 Kalkulator Faktorial", 
            font=("Arial", 18, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Add tabs (Hanya 3 tab tanpa Tentang)
        self.calc_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.calc_tab, text="Kalkulator")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.add(self.stats_tab, text="Statistik")
        
        self.setup_calculator_tab()
        self.setup_history_tab()
        self.setup_statistics_tab()
    
    def setup_calculator_tab(self):
        """Setup tab kalkulator"""
        # Input frame
        input_frame = ttk.Frame(self.calc_tab)
        input_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(
            input_frame, 
            text="Masukkan bilangan bulat non-negatif:",
            font=("Arial", 12),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=10)
        
        self.entry_number = ttk.Entry(
            input_frame,
            font=("Arial", 14),
            width=20
        )
        self.entry_number.pack(pady=10)
        self.entry_number.bind("<Return>", lambda e: self.hitung_faktorial())
        
        # Buttons frame
        button_frame = ttk.Frame(self.calc_tab)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(
            button_frame,
            text="Hitung Faktorial",
            command=self.hitung_faktorial,
            style="Accent.TButton"
        ).pack(side="left", padx=10)
        
        ttk.Button(
            button_frame,
            text="Hapus Input",
            command=self.clear_input,
            style="Danger.TButton"
        ).pack(side="left", padx=10)
        
        # Result frame
        self.result_frame = ttk.Frame(self.calc_tab)
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="Hasil akan ditampilkan di sini...",
            font=("Arial", 14),
            wraplength=800,
            bg=self.bg_color,
            fg=self.fg_color,
            justify="left"
        )
        self.result_label.pack(pady=20, anchor="w")
        
        self.detail_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 11),
            wraplength=800,
            bg=self.bg_color,
            fg="#888888",
            justify="left"
        )
        self.detail_label.pack(pady=10, anchor="w")
    
    def setup_history_tab(self):
        """Setup tab history"""
        # Controls frame
        controls_frame = ttk.Frame(self.history_tab)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(
            controls_frame,
            text="Refresh History",
            command=self.update_history_display
        ).pack(side="left", padx=10)
        
        ttk.Button(
            controls_frame,
            text="Hapus Semua History",
            command=self.clear_all_history,
            style="Danger.TButton"
        ).pack(side="left", padx=10)
        
        # Treeview for history
        tree_frame = ttk.Frame(self.history_tab)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("No", "Input", "Hasil", "Perhitungan", "Waktu")
        self.history_tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show="headings",
            height=15
        )
        
        # Configure columns
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)
        
        self.history_tree.column("Perhitungan", width=200)
        self.history_tree.column("Waktu", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_statistics_tab(self):
        """Setup tab statistik"""
        self.stats_frame = ttk.Frame(self.stats_tab)
        self.stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def hitung_faktorial(self):
        """Menghitung faktorial dan menampilkan hasil"""
        try:
            input_text = self.entry_number.get().strip()
            if not input_text:
                messagebox.showwarning("Peringatan", "Masukkan angka terlebih dahulu!")
                return
            
            n = int(input_text)
            
            if n < 0:
                messagebox.showerror("Error", "Angka tidak boleh negatif!")
                return
            
            if n > 1000:
                if not messagebox.askyesno("Konfirmasi", 
                                          f"Angka {n} sangat besar dan mungkin membutuhkan waktu lama.\nLanjutkan?"):
                    return
            
            # Calculate factorial
            calculator = FaktorialCalculator()
            hasil, penjabaran = calculator.hitung_faktorial(n)
            
            # Format result
            if hasil > 10**6:
                hasil_formatted = calculator.format_angka_besar(hasil)
            else:
                hasil_formatted = f"{hasil:,}".replace(",", ".")
            
            # Display result
            result_text = f"🎉 HASIL: {n}! = {hasil_formatted}"
            detail_text = f"📝 Penjabaran: {penjabaran}"
            
            self.result_label.configure(text=result_text)
            self.detail_label.configure(text=detail_text)
            
            # Save to history
            self.db.save_calculation(n, hasil_formatted, penjabaran)
            
            # Update displays
            self.update_history_display()
            self.update_statistics()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Input tidak valid: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    
    def clear_input(self):
        """Membersihkan input dan hasil"""
        self.entry_number.delete(0, 'end')
        self.result_label.configure(text="Hasil akan ditampilkan di sini...")
        self.detail_label.configure(text="")
    
    def update_history_display(self):
        """Memperbarui tampilan history"""
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get history from database
        history = self.db.get_all_history()
        
        # Populate treeview
        for i, record in enumerate(history, 1):
            self.history_tree.insert("", "end", values=(
                i, record[1], record[2], record[3], record[4]
            ))
    
    def update_statistics(self):
        """Memperbarui tampilan statistik"""
        # Clear existing widgets
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Get statistics
        stats = self.db.get_statistics()
        
        # Create stats display
        title_label = tk.Label(
            self.stats_frame,
            text="📊 STATISTIK PENGGUNAAN",
            font=("Arial", 18, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(pady=20)
        
        stats_text = f"""• Total Perhitungan: {stats['total_perhitungan']} kali
• Angka Tertinggi yang Dihitung: {stats['angka_tertinggi']}
• Perhitungan Terakhir: {stats['terakhir_dihitung']}

💡 Tips: 
- Faktorial 10! = 3.628.800
- Faktorial 20! = 2.432.902.008.176.640.000
- Angka di atas 50! akan sangat besar!"""
        
        stats_label = tk.Label(
            self.stats_frame,
            text=stats_text,
            font=("Arial", 14),
            justify="left",
            bg=self.bg_color,
            fg=self.fg_color
        )
        stats_label.pack(pady=20)
        
        # Add quick actions
        action_frame = ttk.Frame(self.stats_frame)
        action_frame.pack(pady=20)
        
        ttk.Button(
            action_frame,
            text="📊 Lihat History Lengkap",
            command=lambda: self.notebook.select(1)  # Switch to history tab
        ).pack(side="left", padx=10)
        
        ttk.Button(
            action_frame,
            text="🧮 Kalkulator Baru",
            command=lambda: self.notebook.select(0)  # Switch to calculator tab
        ).pack(side="left", padx=10)
    
    def clear_all_history(self):
        """Menghapus semua history"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua history?"):
            self.db.clear_history()
            self.update_history_display()
            self.update_statistics()
            messagebox.showinfo("Sukses", "Semua history telah dihapus!")
    
    def run(self):
        """Menjalankan aplikasi"""
        self.root.mainloop()