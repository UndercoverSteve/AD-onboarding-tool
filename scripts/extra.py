#    for sku in skus:
#        part_number = sku["skuPartNumber"]
#        if part_number == sku_id:
#            chosen_sku = sku
#            break

    # Can't find our sku in returned dictionary of skus
#    if chosen_sku is None:
#        print("sku_id is not valid")
#        return False
#
    # Check to make sure amount of skus isn't at max. If it's at max return fail
#    if chosen_sku["prepaidUnits"]["enabled"] >= sku["consumedUnits"]:
#        print("Max limit of this SKU is reached. Free up a license to assign to this user.")
#       return False