import sys

from typing import NamedTuple

Coupon = NamedTuple("Coupon", [("store", str), ("product", str), ("discount", int)])


def line_to_coupon(line: str) -> Coupon:
    tokens = line.strip().split(";")
    return Coupon(tokens[0], tokens[1], int(tokens[2]))


def coupon_to_line(coupon: Coupon) -> str:
    return f'{coupon.product} ({coupon.store}): {coupon.discount}%'


def sort_coupon(coupons: list[Coupon]) -> list[Coupon]:
    coupons.sort(key=lambda coupon: (coupon.store, -coupon.discount, coupon.product))
    return coupons


def main():
    coupons = []

    # EOF
    for line in sys.stdin:
        coupon = line_to_coupon(line)
        coupons.append(coupon)

    coupons = sort_coupon(coupons)

    for coupon in coupons:
        coupons = coupon_to_line(coupon)
        print(coupons)


if __name__ == "__main__":
    main()
