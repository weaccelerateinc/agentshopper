# Backcountry.com Checkout Flow

## Platform
- Custom platform (likely Salesforce Commerce Cloud)

## URL
- Homepage: https://www.backcountry.com
- Cart: https://www.backcountry.com/cart
- Product pages: e.g., https://www.backcountry.com/camelbak-podium-15oz-water-bottle

## Product Discovery
- Browse by category: Camp > Hydration > Water Bottles
- Sorting available: "Lowest Price", "Highest Rated", "New Arrivals", "Highest Price", "Percent Off"
- Product filtering: By brand, color, sale status, features
- Example cheap product: CamelBak Podium 15oz Water Bottle - $6.00 (50% off, normally $12.00)

## Product Page Structure
- Product image (left side)
- Product info (right side):
  - Brand name
  - Product title
  - Star rating + review link
  - Price (discounted + original price + % off)
  - Sale badge (e.g., "Closeout Sale | Ends 4/6")
  - Color selector
  - Size selector
  - Quantity +/- buttons
  - "Add To Cart" button (primary - green/teal color)
  - "Add To Wishlist" button
  - Badges: "Lowest Price Guarantee", "Free Shipping On Orders Over $69", "Return Policy"

## Add to Cart
- Click "Add To Cart" button on product page
- No immediate success confirmation on page (cart icon in header should update)
- Item added to cart silently

## Cart View
- Access via cart icon (shopping bag) in header top-right
- URL: https://www.backcountry.com/cart
- Shows: Cart items with images, names, prices, quantity selectors
- Cart tabs: "Cart (X)" | "Wish List"
- Empty cart message: "Your cart is currently empty"
- If items present, shows subtotal and checkout buttons

## Checkout Flow (Observed Partial)
The standard flow appears to be:
1. Click "Proceed to Checkout" or similar button (not fully tested)
2. Shipping address entry (required fields: name, address, city, state, zip, phone)
3. Shipping method selection (based on order total and location)
4. Billing address (can be same as shipping)
5. Payment step (card details, CVV, expiry) — **DO NOT FILL THIS OUT FOR TEST**

## Shipping
- Free shipping on orders over $69
- Multiple shipping methods available (standard/expedited)
- Supports US addresses

## Payment Methods
- Credit cards (Visa, Mastercard, American Express, Discover)
- PayPal integration likely available
- No BNPL options observed (subject of test)

## Key Observations
- Requires logged-in account (redirects to signin if not authenticated)
- User account shows "Welcome! Summit Club Member" after signup
- Products display inventory status (in/out of stock)
- Real-time price discounts and sale badges
- Free shipping incentive at $69+
- Clearance/closeout sales common (up to 70% off)

## Test Notes
- CamelBak Podium 15oz Water Bottle found at $6.00 (cheapest water bottle when sorting by price)
- Product is in stock (One Size available)
- "Trending now: 90 are viewing this product" indicator shown
- Adding to cart functioned but cart remained empty on recheck (potential JavaScript issue or session state issue)

## Common Issues
- **Rendering blank pages**: Use JavaScript zoom trick: `document.body.style.zoom='0.7'`
- **Add to cart not working**: May require JavaScript to be fully enabled; try refreshing product page
- **Cart not updating**: Session or cart state may not persist; navigate directly to /cart URL
- **Page responsiveness**: Site can be slow to load and render (especially with images)
- **Modal interactions**: Checkout modals may appear for signup prompts even if already logged in

## Return Policy
- Clearly stated on product pages
- Free returns available (linked in product details)

## Promotions
- Summit Club membership offers 10% cash back on purchases
- First order incentives may be available
- Seasonal clearance sales (up to 70% off observed)
