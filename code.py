import asyncio
import time
 
class DataProcessor:
    def process_data(self, data):
        """Internal processing logic."""
        # Violation: Rule 'Internal Methods' - should start with _
        print(f"Processing {data}")
        return data.strip()
 
    async def handle_request(self, request):
        # Violation: Rule 'Async Safety' - uses blocking time.sleep
        print("Handling request...")
        time.sleep(1)
        result = self.process_data(request)
        return result
 
def main():
    processor = DataProcessor()
    # Violation: Built-in naming standard (Static AST check)
    def Bad_Naming_Function():
        pass
    
    asyncio.run(processor.handle_request("  hello  "))
 
if __name__ == "__main__":
    main()