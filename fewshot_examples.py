fewshot_examples = [
    {
        "question": "What is the total revenue for Levi brand?",
        "sql": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi';",
        "answer": "Total revenue value for Levi brand."
    },
    {
        "question": "How many white shirts from Levi are in stock?",
        "sql": "SELECT SUM(stock_quantity) FROM t_shirts WHERE color = 'White' AND brand = 'Levi';",
        "answer": "Number of white Levi shirts in stock."
    },
    {
        "question": "Show small size total revenue.",
        "sql": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE size = 'S';",
        "answer": "Total revenue for small-size T-shirts."
    },
    {
        "question": "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue our store will generate (post discounts)?",
        "sql": """
            SELECT SUM(a.total_amount * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) AS total_revenue
            FROM (
                SELECT SUM(price * stock_quantity) AS total_amount, t_shirt_id
                FROM t_shirts
                WHERE brand = 'Levi'
                GROUP BY t_shirt_id
            ) a
            LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id;
        """,
        "answer": "The total revenue our store will generate (after discounts) is 17,501.05."
    },
    {
        "question": "How many Adidas red T-shirts do we have in stock?",
        "sql": "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Adidas' AND color = 'Red';",
        "answer": "Number of Adidas red T-shirts in stock."
    }
]
