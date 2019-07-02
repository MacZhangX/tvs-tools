import java.io.File;
import java.io.FileOutputStream;
import java.util.HashMap;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import bean.AIRequest;
import bean.ReqHeader;
import bean.tts.TTSReqPayload;
import tools.Base64Util;
import tools.HttpUtil;
import tools.SignatureTool;

public class TTSSample {
	static String url = "https://aiwx.html5.qq.com/api/tts";

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

		TTSReqPayload payload = new TTSReqPayload("����������ô���� ��Է����𣬹�����");
		boolean isFinish = false;
		String sessionId = "";
		int index = 0;
			
		FileOutputStream fileOutputStream = new FileOutputStream(new File("tts.mp3"));
		
		while (!isFinish) {
			payload.session_id = sessionId;
			payload.index = index;

			req.payload = payload;
			 
			Gson gson = new Gson();
			String body = gson.toJson(req);

			System.out.println(body);

			String authorization = SignatureTool.getAuthorization(Common.appkey, Common.accessToken, body);
			System.out.println("authorization:" + authorization);
			String contentType = SignatureTool.getContentType();
			// ���ͷ��
			HashMap<String, String> customHeaders = new HashMap<String, String>();
			customHeaders.put("Authorization", authorization);
			customHeaders.put("Content-Type", contentType);
			// ��������
			String response = HttpUtil.sendPost(url, body, customHeaders);
			// �ذ�����
			System.out.println(response);

			JsonObject obj = new JsonParser().parse(response).getAsJsonObject();
			
			isFinish = obj.get("payload").getAsJsonObject().get("speech_finished").getAsBoolean();
			String speechBase64 = obj.get("payload").getAsJsonObject().get("speech_base64").getAsString();
			sessionId = obj.get("header").getAsJsonObject().get("session").getAsJsonObject().get("session_id").getAsString();
			index++;
			byte[] speech = Base64Util.decode(speechBase64);
			fileOutputStream.write(speech);
			System.out.println("speechBase64:" + speechBase64.length());
			System.out.println("speech_finished��" + isFinish);

		}
		fileOutputStream.close();
		
	}

	public static void main(String[] args) throws Exception {
		request();
		// ����JSON��
//		System.out.println("sss");

	}

}
