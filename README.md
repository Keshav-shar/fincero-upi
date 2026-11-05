# Fincero

A UPI payments app that teaches you finance while you pay.

Fincero handles your everyday UPI payments. Alongside them runs a shared market where you practise investing with **ceros**, a currency you earn just by using the app.

Fincero is in active development.

## Features

### UPI payments

- Link your bank account and create your UPI ID
- Pay by UPI ID, QR code or phone number
- Receive money, and approve merchant collect requests
- Check your bank balance on demand
- See your transaction history and raise a dispute
- Hear incoming payments announced aloud while the app is open

### Ceros

- Earn 1 cero for each day you open the app
- Earn 1 cero per whole rupee paid to a verified merchant, up to a daily limit
- Spend ceros in the market

### Market

- Trade 5 default stocks, follow a 3-stock index, and invest in mutual funds
- Protect a position with a stop-loss, or short a stock you expect to fall
- Create your own stock for 1,500.00 ceros and write a pitch for buyers
- Pay a daily tax of 1% of your starting amount while your stock is listed
- See price history and trend estimates

The market is shared, so every user sees the same prices. Buying pushes a price up and selling pushes it down, and charts refresh every 20 seconds. Every 20 minutes, each stock also takes a percent update.

### Assistant

Ask the chatbot on your transactions page about your spending, your ceros and the finance behind them. It reads your own data only, and it can't move money.

## Amounts

| Currency | Format | Example |
|----------|--------|---------|
| Rupees | 2 decimals | ₹1,23,456.78 |
| Ceros | 2 decimals | 1,500.00 |

## Tech stack

| Part | Built with |
|------|------------|
| Mobile app | React Native and Expo (TypeScript) |
| Server | C++20 with Drogon |
| Shared logic | C++ core library used by the app and the server |
| Data | PostgreSQL, with Redis for rate limits and live updates |
| Assistant | Anthropic API, called from the server |
| Payments | UPI through a payment service provider |

## Getting started

You need Docker. All C++ tools run inside a pinned image, so nothing else is required to build.

```
git clone https://github.com/Keshav-shar/fincero-upi.git
cd fincero-upi
./dev test
```

The first build compiles every dependency and takes a while. Later builds use a cache.

| Command | What it does |
|---------|--------------|
| `./dev build [preset]` | Configure and build |
| `./dev test [preset]` | Build and run the tests |
| `./dev check` | Check module boundaries, core purity and migrations |
| `./dev format` | Format the C++ code |
| `./dev shell` | Open a shell in the toolchain |

Presets: `dev` (default), `asan`, `tsan`, `fuzz`, `ci`, `ci-gcc`, `release`.

To start the database and cache, set `POSTGRES_PASSWORD` and `REDIS_PASSWORD` in your shell, then run:

```
docker compose up -d postgres redis
```

Both refuse to start without a password. Never commit secrets.

## Project layout

```
core/     shared C++ logic: money, ledger rules, market engine
server/   API server and its modules
client/   React Native app
api/      OpenAPI definition
db/       database migrations
tools/    developer tools
tests/    integration tests and fuzzers
```

## Good to know

- **Ceros are not money.** They can't be bought, cashed out or exchanged for anything of value.
- **The market is an educational simulation, not investment advice.**
- **Your UPI PIN stays private.** You enter it only in the payment partner's secure screen, never in Fincero's own code.
