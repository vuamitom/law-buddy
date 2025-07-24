from llm import generate


def main():
    resp = generate("Thuế VAT cho dịch vụ tư vấn là bao nhiêu?")
    print(resp)


if __name__ == "__main__":
    main()
