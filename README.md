# Marche :: A online Market.

![Logo](static/market-rising-icon.png)

## Model Relationships.
- User :: Default django user model.

- Product:
  - image
  - title
  - description
  - quantity
  - category

- Transaction: 
  - product :: ForeignKey
  - user :: ForeignKey
  - ...

- Category:
  - title
  - products :: ManyToMany

- Cart
  - user
  - products :: ManyToMany

- Wishlist
  - user
  - products :: ManyToMany
  
## Template:
- Landing Page
- Search Page
- Category Page
- Cart Page
- Whislist PAge
- Checkout Page

- Shipper
  - Dashboard 
  - Status

## Building the tailwind.css file:
```bash
npx tailwindcss build styles.css -o output.css
```

