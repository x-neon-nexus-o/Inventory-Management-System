import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import customtkinter as ctk  # Add this import


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

    # Inside the add_graphs function where the pie chart is created
    try:
        # Execute the query to get counts for both statuses, ensuring both are included
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

        # Extract labels and data, ensuring both "Paid" and "Pending" are present
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

        # Add missing statuses with count 0
        if not found_paid:
            order_status.append('Paid')
            order_count.append(0)
        if not found_pending:
            order_status.append('Pending')
            order_count.append(0)

        # Create pie chart with both statuses
        pie_fig = plt.Figure(figsize=(4, 4), dpi=100)
        ax1 = pie_fig.add_subplot(1, 1, 1)
        ax1.pie(order_count, labels=order_status, autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
                colors=[colors[0], colors[1]], startangle=90)
        ax1.set_title("Order Status")

        # Create a frame to hold the pie chart and legend
        pie_container = ctk.CTkFrame(master=graph_container, fg_color="transparent")
        pie_container.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # Embed the chart in the Tkinter frame
        pie_canvas = FigureCanvasTkAgg(pie_fig, master=pie_container)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Create legend frame
        legend_frame = ctk.CTkFrame(master=pie_container, fg_color="transparent")
        legend_frame.pack(pady=(10, 0))

        # Add legend items
        legend_items = [
            {"color": colors[0], "label": "Paid"},
            {"color": colors[1], "label": "Pending"}
        ]

        for item in legend_items:
            # Create a frame for each legend item
            item_frame = ctk.CTkFrame(master=legend_frame, fg_color=item["color"], width=20, height=20)
            item_frame.pack(side="left", padx=(0, 10), pady=5)

            # Create label for the legend item
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

        # Corrected SQL query to order by month
        cur.execute("""
            SELECT DATE_FORMAT(o.date, '%b') AS month, 
                   SUM(oi.quantity * oi.price) AS earnings 
            FROM orders o 
            JOIN order_items oi ON o.order_id = oi.order_id 
            WHERE o.payment_status = 'paid' 
              AND YEAR(o.date) = YEAR(CURDATE()) 
            GROUP BY month 
            ORDER BY month
        """)
        results = cur.fetchall()

        earnings = [0] * 12
        for month, earning in results:
            try:
                index = months.index(month)
                earnings[index] = earning
            except ValueError:
                pass  # Skip invalid month names

        # Create bars with month names and earnings
        bars = ax2.bar(months, earnings, color=colors)

        # Add earnings values on top of each bar
        for bar, earning in zip(bars, earnings):
            if earning != 0:
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f"₹{earning:.2f}", ha='center', va='bottom')

        ax2.set_xlabel("Months")
        ax2.set_ylabel("Earnings (₹)")
        ax2.set_title("Monthly Earnings")
        ax2.grid(True, linestyle='--', alpha=0.7)

        # Rotate month labels for better readability
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

        bar_canvas = FigureCanvasTkAgg(bar_fig, master=graph_container)
        bar_canvas.draw()
        bar_canvas.get_tk_widget().pack(side="right", padx=20, pady=20)
    except Exception as e:
        print(f"Error creating bar graph: {e}")
        error("Failed to generate monthly earnings graph")