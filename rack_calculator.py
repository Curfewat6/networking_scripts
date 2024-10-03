import argparse

wkw_rack_bible = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6'}

def get_rack_information():
    parser = argparse.ArgumentParser(description='Enter your rack information')
    parser.add_argument('rack', type=str, help='Enter your rack number. See the networking rack sticker (example: 7B)')
    args = parser.parse_args()
    return args.rack

def convert_rack_to_numerical(rack_id):
    rack_code = rack_id
    letter = rack_code[-1]
    number = wkw_rack_bible[letter.upper()]
    return rack_code[0] + number

def display_results(rack_id, results):
    header = "| {:<30} | {:<30} |".format("What we calculated for you", "The thing you are looking for")
    divider = "+" + "-" * 32 + "+" + "-" * 32 + "+"

    data = [
        ("Rack Number", rack_id),
        ("Edge router to ISP network", f"172.17.9.{results['internal_to_ISP']}/30"),
        ("Edge router's IP", f"172.17.9.{int(results['internal_to_ISP']) + 1}/30"),
        ("ISP's IP", f"172.17.9.{int(results['internal_to_ISP']) + 2}/30"),
        ("Public IP Block", f"203.149.{results['quotient'] + 210}.{results['remainder']}/29"),
        ("First Usable Public IP", f"203.149.{results['quotient'] + 210}.{results['remainder'] + 1}/29"),
        ("Last Usable Public IP", f"203.149.{results['quotient'] + 210}.{results['remainder'] + 6}/29")
    ]

    # Print the table
    print(divider)
    print(header)
    print(divider)
    for item, value in data:
        print("| {:<30} | {:<30} |".format(item, value))
    print(divider)



def main():
    print("[*] Running Raw!")
    results = {'internal_to_ISP': None, 'quotient': None, 'remainder': None}

    rack_id = get_rack_information()
    print(f"[*] Your rack number is: {rack_id}")
        
    # Convert to octal
    octal = convert_rack_to_numerical(rack_id)

    # Convert to numerical
    numerical = (int(octal[0]) * 8) + int(octal[1])

    # Determine the last octet
    last_octet = numerical * 4
    results ['internal_to_ISP'] = last_octet

    # Determine the public IP address block
    numerical = numerical * 8
    quotient = numerical // 256
    remainder = numerical % 256
    results['quotient'] = quotient
    results['remainder'] = remainder

    display_results(rack_id, results)
    
if __name__ == '__main__':
    main()