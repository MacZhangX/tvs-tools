import java.util.HashMap;
import com.google.gson.Gson;

import bean.AIRequest;
import bean.ReqHeader;
import bean.richanswer.RichAnswerReqPayload;
import tools.HttpUtil;
import tools.SignatureTool;

 

public class RichAnswerSample {
	
    static String url = "https://aiwx.html5.qq.com/api/v1/richanswerV2";
	static void request() throws Exception {
		// ��װ�����ʽ��
		AIRequest req = new AIRequest();
		ReqHeader header = new ReqHeader();
		// �豸���к�
		header.device.serial_num = "abcedfg";
		header.qua = "QV=3&VE=GA&VN=1.0.0.1000&PP=com.tencent.ai.tvs&CHID=10020";
		// ����ͨ���ƶ˵��õģ���Ҫ���ն˵�ip��ַ���ȥ��
//		header.ip = "1.2.3.4";
		
		// �����ѡ����ҪLBS��Ϣ�ļ��ܣ��絼�����ն�LBS�Ǳ���ġ�
//		header.lbs = new LBSInfo();
//		header.lbs.latitude = 3.0;
//		header.lbs.longitude = 3.0;
		
		
		
		req.header = header;
		req.payload = new RichAnswerReqPayload("���");
        Gson gson = new Gson();
        String body = gson.toJson(req);
        
        System.out.println(body);
        
        String authorization = SignatureTool.getAuthorization(Common.appkey, Common.accessToken, body);
        System.out.println("authorization:"+authorization);
        String contentType = SignatureTool.getContentType();
        // ���ͷ��
        HashMap<String, String> customHeaders= new HashMap<String, String>();
        customHeaders.put("Authorization", authorization);
        customHeaders.put("Content-Type", contentType);
        // ��������
        String response = HttpUtil.sendPost(url, body, customHeaders);
        // �ذ�����
        System.out.println(response);

			
	}
	public static void main(String[] args) throws Exception {
		request();
        
        	
	}

}
