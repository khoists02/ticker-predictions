ALTER TABLE sessions ADD CONSTRAINT sessions_unique UNIQUE(ticker, date_time, date, current_price, previous_price);