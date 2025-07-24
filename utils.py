import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import customtkinter as ctk

def error(text):
    """Creates an error message box and print the error."""
    print(f"[!]   {text}!")
    messagebox.showerror("[ Error ]", text)

def add_graphs(cur, frame):
    plt.style.use("dark_background")
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'

    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#1a1a1a'

    colors = [
        "#FF5A5F",  # Red
        "#0079BF",  # Blue
        "#00C2E0",  # Teal
        "#51E898",  # Green
        "#F2D600",  # Yellow
        "#FF7A5A",  # Orange
        "#A652BB",  # Purple
        "#EB5A46",  # Coral
        "#FFD500",  # Gold
        "#8ED1FC",  # Sky Blue
    ]

    # Clear previous graphs if any
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a container frame for graphs
    graph_container = ctk.CTkFrame(master=frame, fg_color="transparent")
    graph_container.pack(fill="both", expand=True, padx=20, pady=20)

    # Pie Chart for Order Status
    try:
        cur.execute("""
            SELECT 
                CASE 
                    WHEN payment_status = 'paid' THEN 'Paid' 
                    WHEN payment_status = 'pending' THEN 'Pending' 
                    ELSE 'Other' 
                END AS status,
                COUNT(*) AS count 
            FROM orders 
            GROUP BY status
            WITH ROLLUP;
        """)
        payments = cur.fetchall()

        order_status = []
        order_count = []
        found_paid = False
        found_pending = False

        for row in payments:
            if row[0] == 'Paid':
                order_status.append('Paid')
                order_count.append(row[1])
                found_paid = True
            elif row[0] == 'Pending':
                order_status.append('Pending')
                order_count.append(row[1])
                found_pending = True

        if not found_paid:
            order_status.append('Paid')
            order_count.append(0)
        if not found_pending:
            order_status.append('Pending')
            order_count.append(0)

        pie_fig = plt.Figure(figsize=(4, 4), dpi=100)
        ax1 = pie_fig.add_subplot(1, 1, 1)
        ax1.pie(order_count, labels=order_status, autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
                colors=[colors[0], colors[1]], startangle=90)
        ax1.set_title("Order Status")

        pie_container = ctk.CTkFrame(master=graph_container, fg_color="transparent")
        pie_container.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        pie_canvas = FigureCanvasTkAgg(pie_fig, master=pie_container)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack(fill="both", expand=True)

        legend_frame = ctk.CTkFrame(master=pie_container, fg_color="transparent")
        legend_frame.pack(pady=(10, 0))

        legend_items = [
            {"color": colors[0], "label": "Paid"},
            {"color": colors[1], "label": "Pending"}
        ]

        for item in legend_items:
            item_frame = ctk.CTkFrame(master=legend_frame, fg_color=item["color"], width=20, height=20)
            item_frame.pack(side="left", padx=(0, 10), pady=5)
            label = ctk.CTkLabel(master=legend_frame, text=item["label"], font=("Century Gothic", 12))
            label.pack(side="left", padx=(0, 20))

    except Exception as e:
        print(f"Error creating pie chart: {e}")
        error("Failed to generate order status chart")

    # Bar Graph for Monthly Earnings
    try:
        bar_fig = plt.Figure(figsize=(7, 4), dpi=100)
        ax2 = bar_fig.add_subplot(1, 1, 1)
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        cur.execute("""
            SELECT DATE_FORMAT(o.date, '%b') AS month, 
                   SUM(oi.quantity * oi.price) AS earnings 
            FROM orders o 
            JOIN order_items oi ON o.order_id = oi.order_id 
            WHERE o.payment_status = 'paid' 
              AND YEAR(o.date) = YEAR(CURDATE()) 
            GROUP BY month 
            ORDER BY FIELD(month, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        """)
        results = cur.fetchall()

        earnings = [0] * 12
        for month, earning in results:
            try:
                index = months.index(month)
                earnings[index] = float(earning) if earning else 0
            except ValueError:
                pass

        bars = ax2.bar(months, earnings, color=colors)

        ax2.set_xlabel("Months")
        ax2.set_ylabel("Earnings (₹)")
        ax2.set_title("Monthly Earnings")
        ax2.grid(True, linestyle='--', alpha=0.7)
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

        # Add hover tooltip functionality
        def on_hover(event):
            if event.inaxes == ax2:
                for bar in bars:
                    contains, _ = bar.contains(event)
                    if contains:
                        value = bar.get_height()
                        ax2.annotate(
                            f'₹{value:,.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                            xytext=(0, 5),
                            textcoords='offset points',
                            ha='center',
                            bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8),
                            fontsize=10
                        )
                        bar_fig.canvas.draw_idle()
                        return
                # Remove any existing annotations
                for annot in ax2.texts:
                    annot.remove()
                bar_fig.canvas.draw_idle()

        bar_fig.canvas.mpl_connect('motion_notify_event', on_hover)

        bar_canvas = FigureCanvasTkAgg(bar_fig, master=graph_container)
        bar_canvas.draw()
        bar_canvas.get_tk_widget().pack(side="right", padx=20, pady=20)

    except Exception as e:
        print(f"Error creating bar graph: {e}")
        error("Failed to generate monthly earnings graph")