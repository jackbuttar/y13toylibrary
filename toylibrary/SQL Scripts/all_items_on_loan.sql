SELECT Items.item_id, items.Item, items.Type, items.[Rental Price]
FROM Items
JOIN rentals ON rentals.Item_ID = items.Item_ID
WHERE rentals.[Returned Date] IS NULL