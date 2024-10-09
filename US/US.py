from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

@app.get("/fibonacci")
def fibonacci(
    hostname: str = Query(...),
    fs_port: int = Query(...),
    number: int = Query(...),
    as_ip: str = Query(...),
    as_port: int = Query(...)
):
    try:

        print(f"Received parameters: hostname={hostname}, fs_port={fs_port}, number={number}, as_ip={as_ip}, as_port={as_port}")

        dns_query_url = f'http://{as_ip}:{as_port}/dns-query'
        print(f"Querying DNS at: {dns_query_url}")

        dns_response = requests.get(dns_query_url, params={'name': hostname, 'type': 'A'})
        print(f"DNS response status: {dns_response.status_code}")

        if dns_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to query authoritative server")

        dns_data = dns_response.json()
        fibonacci_ip = dns_data.get('value')

        if not fibonacci_ip:
            raise HTTPException(status_code=404, detail="Fibonacci server IP not found")

        fibonacci_url = f'http://{fibonacci_ip}:{fs_port}/fibonacci'
        print(f"Querying Fibonacci server at: {fibonacci_url}")

        fibonacci_response = requests.get(fibonacci_url, params={'number': number})
        print(f"Fibonacci response status: {fibonacci_response.status_code}")

        if fibonacci_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to get Fibonacci number")

        result = fibonacci_response.json().get('result')
        return {"fibonacci_number": result}
    
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
