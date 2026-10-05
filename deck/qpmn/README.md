# Printing the deck through QP Market Network

QPMN (qpmarketnetwork.com) is the print-on-demand platform of QP Group, the
Hong Kong manufacturer that also owns MakePlayingCards. It prints and ships
each order white-label, with no minimum, and exposes a REST API. Researched
from its own pages on 2026-10-01; every figure below is from those pages.

## Facts that matter for this deck

- **Tarot product:** "Tarot Cards (2.75" x 4.75")", product id 146829203.
  Deck presets 10 to 160 cards; 121 is not a preset, so use "Custom" or 130.
- **Files:** the template is 2.99 x 4.99 in = **897 x 1497 px at 300 DPI**,
  cut at 825 x 1425, safe area 753 x 1353. JPG, PNG or PDF. `deck/print-qpmn/`
  holds the deck resampled to exactly that size. Whether 900 x 1500 would be
  accepted as-is is not published.
- **Unique backs:** "Design every card front and back with your own artwork";
  oracle decks may "use either unique backs or one shared back". No surcharge
  is mentioned. Still to confirm in the API schema (see below).
- **Stocks:** PS30 (300 gsm blue core, the default), DS33 330 gsm black core,
  linen 280/290/310, SL35 350 gsm, EF27 eco, plastic. Foils and gilt edges
  are options. Tuck boxes printed outside or both sides; rigid boxes.
- **Turnaround:** 2 to 5 business days production, 7 to 12 days shipping from
  southern China, tracked. US orders carry a 10% "Import Service fee" at
  checkout. Prices are only shown inside an account ("Tiered Price Table").
- **No fees for the API** beyond product and shipping. You set the retail
  price in your own store and pay QPMN the base cost per order.

## What the account now holds (set up 2026-10-01)

- Partner account registered by Anthony; store **the-pattern-deck**, type
  API Integration, id **751463488**, currency USD.
- Store product **751481485**: Tarot Cards 2.75 x 4.75, PS30 stock, 121 cards,
  full colour both sides, matte, **custom tuck box** (printed outside, T30
  aqueous matte, full colour), shrink-wrapped. Active.
- Price per deck at that configuration, from the tiered table: 1 to 5 decks
  $57.88 with the box ($40.07 without); the dashboard quotes $29.15 at 50 per
  combined order. Shipping and the 10% US import fee are extra.
- `design-schema.json` and `sample-order.json` are the product's own schema and
  sample, pulled from the dashboard. They settle three things:
  - **Card images are 3.0 x 5.0 in at 300 DPI, i.e. exactly 900 x 1500 px**, so
    `deck/print/` uploads as-is. (`print-qpmn/` at 897 x 1497 is for MPC.)
  - **The tuck box takes one 9.59 x 9.85 in image** (2877 x 2955 px), a flat
    wrap for their "dynamic" box. The dieline is not on the public template
    page; ask QPMN for it or pull it from their design tool.
  - **`Card_Back` has qty 1: this product prints ONE shared back.** Our deck
    has a unique back per card. Either QPMN has a variant with 121 backs (ask),
    or the QPMN edition uses a uniform emblem back with the text in a booklet,
    or the deck is printed where unique backs are supported (MPC, Game Crafter,
    DriveThruCards all do, per the earlier research).
- The sample order shape: top-level `externalId`, `externalOrderNumber`,
  `shippingMethod`, `paymentMethod` ("PayPal"), `currency`, `deliveryAddress`,
  `billingAddress`, `priceInfo`, and `items[]` each with `storeProductId`,
  `quantity`, `unitPrice` and `productDesignData.designData[]` keyed by the
  material codes in the schema. Images are referenced by `imageUrl` and the
  effect is `"CMYK"`.

## How the API works (as published)

- Register as a partner, create a store of type **Api Integration**, add the
  tarot product to it as a "SKU without design".
- The dashboard then gives, per product, an **API Document**, a **sample order
  JSON**, and a **Design Schema** describing each material (Card), its views
  (`Card_Front`, `Card_Back`), how many images each view takes (`qty`), the
  image size/DPI/formats, and the print effect (`CMYK`).
- An order is a JSON POST with the customer, the shipping address, the product,
  and **Design Data**: for each view, a list of designs indexed from 0, each
  carrying the **URL** of the print image. Images are fetched by URL, not
  uploaded. Hosting rules (public, expiry, size) are not published.
- Not published anywhere: base URL, auth header format, order-status or
  tracking endpoints, webhooks (none mentioned), rate limits, a sandbox. The
  team sends the per-product reference on request.

`qpmn_order.py` builds Design Data from `manifest.csv` once the schema is in
hand: it maps every card's front and back to the right view and index.

## What only the account holder can do

1. Register at https://www.qpmarketnetwork.com/app/partner/regist and
   activate by email. Nickname, email, password; no business details asked.
2. Create an **Api Integration** store, add product 146829203, make a SKU.
3. Products > My Products > Actions > **API Document**: save the sample order
   JSON and download the Design Schema. That answers whether `Card_Back` takes
   121 images.
4. Ask QPMN (contact form, or WhatsApp +1 236-978-0709) for the WhiteLabel API
   documentation for the tarot product: base URL, auth, order creation,
   status and tracking, image hosting rules, sandbox.
5. On the product page, pick the stock, a Custom quantity of 121, full colour
   both sides and a tuck box, and read the tiered price and US shipping for
   1, 10, 100 and 500 decks.
6. Confirm how production orders are paid (USD; card via PayPal is implied).

Until then, a proof deck can be ordered by hand on MakePlayingCards with the
same files; its template is identical.
