/* The Cookiee Club: catalogue for the v2 concept.
   Prices and flavour lists match thecookieeclub.com on 12 Oct 2026.
   Stock states are demo values: in Shopify they come from inventory. */
window.TCC = {
  shipping: 16.20,           // flat express post (per Ruby's FAQ; confirm flat vs weight-based)
  turnaround: '2 to 4 business days',
  restock: '[day] 7pm AEST',

  flavours: [
    { id: 'caramello-koala',      name: 'Caramello Koala',      desc: 'Vanilla cookie, a Caramello Koala, milk chocolate and gooey caramel.', img: 'caramello-koala', best: true },
    { id: 'mini-mm',              name: 'Mini M&M',             desc: 'The classic vanilla cookie, packed with Mini M&M’s.', img: 'mini-mm', best: true },
    { id: 'fairy-bread',          name: 'Fairy Bread',          desc: 'The Aussie favourite: pink frosting and plenty of sprinkles.', img: 'fairy-bread', best: true },
    { id: 'cinnamon-scroll',      name: 'Cinnamon Scroll',      desc: 'A cinnamon-swirled cookie finished with a sweet glaze.', img: null, best: true },
    { id: 'chocolate-chip',       name: 'Chocolate Chip',       desc: 'Mum’s cookie, loaded with chocolate chips.', img: 'chocolate-chip' },
    { id: 'marvellous-creations', name: 'Marvellous Creations', desc: 'Topped with Cadbury Marvellous Creations and a chocolate drizzle.', img: 'marvellous-creations' },
    { id: 'biscoff-white-choco',  name: 'Biscoff White Choco',  desc: 'Biscoff and white chocolate.', img: null },
    { id: 'oreo-milkshake',       name: 'Oreo Milkshake',       desc: 'Cookies-and-cream, milkshake style.', img: null },
    { id: 'plain-vanilla',        name: 'Plain Vanilla',        desc: 'Mum’s vanilla cookie, nothing on top.', img: null }
  ],

  products: [
    { id: 'byo12', handle: 'build-your-own-12', name: 'Build Your Own (12)', short: 'Pick any 12 flavours', cookies: 12,
      price: 74.95, compare: 79.90, builder: 12, stock: 'in', badge: 'Best value full box', group: ['build'],
      imgs: ['byo12_0', 'byo12_1', 'byo12_2', 'byo12_3'],
      intro: 'Twelve cookies, your flavours, one parcel. It’s two six-boxes for $4.95 less, and you pay for shipping once.',
      alt: ['A tray of Fairy Bread cookies', 'Caramello Koala cookies cooling on a tray', 'Glazed cookies on a board', 'Six sealed cookies with holographic stickers'] },

    { id: 'byo6', handle: 'build-your-own-6', name: 'Build Your Own (6)', short: 'Pick any six flavours', cookies: 6,
      price: 39.95, builder: 6, stock: 'in', group: ['build'],
      imgs: ['byo6_0', 'byo6_1', 'byo6_2', 'byo6_3'],
      intro: 'Six cookies, any mix of the menu. Pick one of everything you’ve been eyeing, or six of the one you can’t stop thinking about.',
      alt: ['Caramello Koala cookies on a board', 'A plate of Mini M&M cookies', 'Marvellous Creations cookies with the chocolate bars', 'A hand holding a Caramello Koala cookie'] },

    { id: 'gf', handle: 'gluten-free-range', name: 'Gluten Free Range', short: 'Choc Chip, Fairy Bread, Churro, Mini M&M', cookies: 4,
      price: 40, stock: 'in', badge: 'Gluten free', group: ['gf'],
      fixed: ['chocolate-chip', 'fairy-bread', 'cinnamon-churro', 'mini-mm'],
      imgs: ['gf_1', 'gf_0', 'gf_2', 'gf_3'],
      intro: 'Four gluten-free cookies, baked in their own space in our kitchen. Same flavours you know, without the gluten.',
      alt: ['Gluten-free Cinnamon Churro cookies', 'Gluten-free Fairy Bread cookies', 'Gluten-free Mini M&M cookies', 'Gluten-free Chocolate Chip cookies'] },

    { id: 'little', handle: 'the-little-cookiee-club', name: 'The Little Cookiee Club', short: '4 flavours made for kids', cookies: 4,
      price: 30, stock: 'in', badge: 'New', group: ['kids'],
      fixed: ['smiley-face', 'mini-mm', 'plain-vanilla', 'fairy-bread'],
      imgs: ['little_0', 'little_1', 'little_2'],
      intro: 'A little box for our littlest cookie lovers: four fun flavours, made without eggs or nuts.',
      alt: ['Smiley Face cookies with banana lollies', 'Pink frosted Fairy Bread cookies', 'Mini M&M cookies'] },

    { id: 'imperfect', handle: 'the-imperfect-box', name: 'The Imperfect Box', short: '4 wonky ones. Same taste.', cookies: 4,
      price: 12.95, stock: 'out', badge: 'One per customer', limit: 1, group: ['extras'],
      variants: [{ id: 'reg', name: 'Regular', price: 12.95 }, { id: 'gf', name: 'Gluten free', price: 14.95 }],
      imgs: ['imperfect_0', 'imperfect_1', 'imperfect_2', 'imperfect_3'],
      intro: 'Every week some cookies break, spread too thin or come out uneven. They taste exactly the same, so they go in here.',
      alt: ['A mix of imperfect cookies, each sealed', 'A cracked Oreo cookie in its bag', 'A broken Mini M&M cookie', 'Imperfect gluten-free cookies'] },

    { id: 'moulds', handle: 'cookiee-moulds', name: 'Our Cookiee Moulds', short: 'The silicone moulds we bake in', cookies: 0,
      price: 16.95, stock: 'in', badge: 'Pre-order', group: ['extras'],
      imgs: ['moulds_0'],
      intro: 'The six-hole silicone moulds behind our flat, chewy cookies. Pre-order: dispatched within 5 to 7 days, then express post.',
      alt: ['A six-hole silicone cookie mould'] }
  ],

  // Flavours only sold inside fixed boxes (not in the builder)
  extraFlavours: [
    { id: 'midnight-monster', name: 'Midnight Monster', desc: 'Double chocolate with candy eyes.', img: 'midnight-monster' },
    { id: 'trick-or-treat',   name: 'Trick or Treat',   desc: 'White chocolate drizzle and a lolly on top.', img: 'trick-or-treat' },
    { id: 'cinnamon-churro',  name: 'Cinnamon Churro',  desc: 'Cinnamon buttercream piped in a swirl.', img: 'cinnamon-churro' },
    { id: 'smiley-face',      name: 'Smiley Face',      desc: 'Pink icing, sprinkles and a lolly smile.', img: 'smiley-face' }
  ]
};
