package tools;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

public class SignatureTool {

	public static String getAuthorization(String appkey, String accessToken, String body) throws Exception {
		// ��һ����ȡʱ���
		Date date = new Date();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd'T'HHmmss'Z'");
		// ����ʱ��Ϊ0��
		sdf.setTimeZone(TimeZone.getTimeZone("Etc/GMT"));
		String dateStr = sdf.format(date);
		System.out.println("ǩ��ʱ�����" + dateStr);

		// �ڶ�����ƴ��ǩ����

		String signContent = body + dateStr;
		// ������������ǩ����Ϣ

		String signature = HMacSha256.HMACSHA256(signContent, accessToken);

		// ���Ĳ���ƴ��Authorization��

		String authorization = "TVS-HMAC-SHA256-BASIC CredentialKey=" + appkey + ", Datetime=" + dateStr
				+ ", Signature=" + signature;

		return authorization;
	}

	public static String getContentType() {
		return "Content-Type: application/json; charset=UTF-8";
	}
}
