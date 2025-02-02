import cx_Oracle
from db.db_connection import DBConnection


def insert_gold_layer():
    db = DBConnection(user="hr", password="hr", dsn="localhost:1521/XEPDB1")
    try:
        # Conectar ao banco de dados
        connection = db.get_connection()
        cursor = connection.cursor()

        # Obter a maior data já inserida na Gold Layer
        cursor.execute("SELECT MAX(ds) FROM GOLD_APP_USAGE")
        max_ds = cursor.fetchone()[0]

        # Definir filtro de data para pegar apenas os dados novos
        filter_date_condition = f"WHERE datetime > '{max_ds}'" if max_ds else ""

        # Consulta para inserir os dados na Gold Layer
        insert_query = f"""
        INSERT INTO GOLD_APP_USAGE (
            nome_limpo,
            datetime,
            total_eventos,
            tempo_medio_minutos,
            horario_pico,
            evento_mais_frequente,
            ds
        )
        SELECT DISTINCT 
            e.nome_limpo,
            t.datetime,
            c.total_eventos, 
            COALESCE(t.tempo_medio_minutos, 0) AS tempo_medio_minutos,
            p.hora AS horario_pico, 
            f.event_type AS evento_mais_frequente,
            CURRENT_DATE AS ds
        FROM (
            WITH cleaned_events AS (
                SELECT 
                    REGEXP_REPLACE(spau.package_name, '^(com\.|.*\.)', '') AS nome_limpo,
                    spau.datetime,
                    spau.event_type,
                    TO_CHAR(spau.datetime, 'YYYY-MM-DD HH24:MI:SS') AS data_hora,
                    TO_CHAR(spau.datetime, 'HH24') AS hora
                FROM SILVER_PROCESSED_APP_USAGE spau
            ), 
            duration_events AS (
                SELECT 
                    nome_limpo,
                    event_type,
                    datetime,
                    LEAD(datetime) OVER (PARTITION BY nome_limpo ORDER BY datetime) AS proximo_evento,
                    EXTRACT(SECOND FROM (LEAD(datetime) OVER (PARTITION BY nome_limpo ORDER BY datetime) - datetime)) / 60 AS tempo_uso_minutos
                FROM cleaned_events
                WHERE event_type = 'ACTIVITY_RESUMED'
            ), 
            events_count AS (
                SELECT 
                    nome_limpo,
                    COUNT(*) AS total_eventos
                FROM cleaned_events
                GROUP BY nome_limpo
            ), 
            average_time AS (
                SELECT 
                    nome_limpo,
                    datetime,
                    ROUND(AVG(tempo_uso_minutos), 2) AS tempo_medio_minutos
                FROM duration_events
                WHERE tempo_uso_minutos IS NOT NULL
                GROUP BY nome_limpo, datetime
            ), 
            usage_peak AS (
                SELECT 
                    hora,
                    COUNT(*) AS total_eventos_por_hora
                FROM cleaned_events
                GROUP BY hora
            ), 
            event_frequency AS (
                SELECT 
                    event_type,
                    COUNT(*) AS total_eventos_por_tipo
                FROM cleaned_events
                GROUP BY event_type
            )
            SELECT 
                e.nome_limpo,
                t.datetime,
                c.total_eventos, 
                COALESCE(t.tempo_medio_minutos, 0) AS tempo_medio_minutos,
                p.hora AS horario_pico, 
                f.event_type AS evento_mais_frequente
            FROM cleaned_events e
            LEFT JOIN events_count c ON e.nome_limpo = c.nome_limpo
            LEFT JOIN average_time t ON e.nome_limpo = t.nome_limpo
            LEFT JOIN usage_peak p ON e.hora = p.hora
            LEFT JOIN event_frequency f ON e.event_type = f.event_type
            {filter_date_condition}
        ) t
        ON CONFLICT (nome_limpo, datetime) DO NOTHING;
        """

        # Executar a consulta de inserção
        cursor.execute(insert_query)
        conn.commit()

        print(f"Inserção concluída com sucesso! Dados novos foram adicionados.")

    except psycopg2.Error as e:
        print(f"Erro ao executar a consulta: {e}")
    finally:
        # Fechar a conexão com o banco
        if conn:
            cursor.close()
            conn.close()