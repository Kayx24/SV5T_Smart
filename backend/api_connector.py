import requests
import logging
from typing import List, Dict, Any, Optional

# Giả sử bạn đã cấu hình logging trong hệ thống
logger = logging.getLogger(__name__)

class BTCDataConnector:
    """
    Module kết nối và lấy dữ liệu ứng viên từ API của Ban tổ chức (BTC).
    """
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.timeout = 15 # Set timeout cứng để tránh treo hệ thống

    def fetch_students_data(self, endpoint: str = "/api/v1/candidates", params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Lấy danh sách dữ liệu sinh viên từ API.
        Hỗ trợ truyền thêm params (ví dụ: page, limit, year).
        """
        url = f"{self.base_url}{endpoint}"
        raw_data = []

        try:
            logger.info(f"Bắt đầu fetch dữ liệu từ BTC API: {url}")
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            
            # Bắt các lỗi HTTP (401, 403, 404, 500...)
            response.raise_for_status() 
            
            # Giả định API trả về JSON có dạng {"status": "success", "data": [...]}
            json_resp = response.json()
            raw_data = json_resp.get("data", [])
            
            logger.info(f"Fetch thành công {len(raw_data)} bản ghi.")
            return raw_data

        except requests.exceptions.Timeout:
            logger.error("Lỗi Timeout: Server BTC phản hồi quá lâu.")
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Lỗi HTTP từ phía server BTC: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Lỗi kết nối mạng: {req_err}")
        except ValueError:
            logger.error("Lỗi parse JSON: Dữ liệu trả về không đúng định dạng.")
        
        # Nếu có lỗi, trả về list rỗng để Pipeline không bị sập (Graceful Degradation)
        return []

# --- HƯỚNG DẪN TÍCH HỢP VÀO NORMALIZER ---
# Trong main.py hoặc batch_processor.py, bạn sẽ gọi nó như sau:
#
# connector = BTCDataConnector(base_url=config.BTC_API_URL, api_key=config.BTC_API_KEY)
# raw_json_data = connector.fetch_students_data(params={"year": 2026, "status": "submitted"})
# 
# if raw_json_data:
#     normalized_data = universal_normalizer.process_json(raw_json_data)
#     database.save(normalized_data)