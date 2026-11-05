# Fincero

A UPI payments app that teaches you finance while you pay.

Fincero works like any UPI app for real payments. Alongside it runs a simulated economy of **ceros**, a practice currency you earn by using the app and spend on a shared, simulated stock market.

## What you can do

**Payments (₹)**
- Link your bank account and pay or receive through UPI ID, QR code or phone number
- Check your bank balance and see your transaction history
- Hear incoming payments announced out loud while the app is open

**Ceros**
- Earn 1 cero every day you open the app
- Earn ceros when you pay a merchant, based on the amount you pay
- Spend ceros in the market (see below)

**Market simulation**
- Buy and sell 5 default stocks, with stop-loss, price history and trend predictions
- Follow a 3-stock index and invest in mutual funds
- Create your own stock for 1500 ceros and write a pitch to attract buyers
- Creators pay a daily tax of 1% of their starting amount, which keeps the market moving
- Everyone sees the same market, and prices move on a fixed digit sequence built from pi and √2

**Assistant**
- On the previous-transactions page, ask the chatbot about your own spending and payments. It only answers questions about your transactions, ceros and the finance behind them.

## How amounts are shown

| Currency | Format | Example |
|----------|--------|---------|
| Rupees | 2 decimals | ₹1,234.50 |
| Ceros | 5 decimals | 1,500.00000 |

## Tech stack

| Part | Built with |
|------|------------|
| Mobile app | React Native (TypeScript) |
| Server | C++20 with Drogon |
| Shared logic | C++ core library used by both the app and the server |
| Database | PostgreSQL, with Redis for caching |
| Assistant | Anthropic API, called from the server |
| Payments | UPI through a payment service provider |

## Getting started

You will need Node.js (LTS), pnpm, CMake, Ninja, a C++20 compiler, vcpkg, Docker, and Android Studio for running the app on Android.

**1. Clone and configure**

```
git clone <repo-url>
cd fincero
cp .env.example .env
```

Open `.env` and fill in your database URL, Redis URL and Anthropic API key. Never commit this file.

**2. Start the database and cache**

```
docker compose up -d postgres redis
```

**3. Build and run the server**

```
cmake --preset dev
cmake --build --preset dev
./build/dev/server/fincero_server
```

**4. Run the app**

```
cd client
pnpm install
pnpm android
```

**5. Run the tests**

```
ctest --preset dev --output-on-failure     # server and core
cd client && pnpm test                     # app
```

## Project layout

```
core/         shared C++ logic (money, ledger rules, market engine)
server/       API server
sandbox_psp/  UPI simulator for development
client/       React Native app
db/           database migrations
docs/         specs and design notes
```

## Good to know

- **Ceros are not money.** They can't be bought, cashed out or exchanged for anything of value.
- **Not investment advice.** The market is a simulation made for learning.
- **Development uses a simulated UPI service.** Real payments need an approved payment partner and its SDK. Your UPI PIN is only ever entered in the partner's secure screen, never in Fincero's own code.
