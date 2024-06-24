package com.shakespeare.action.collection;

import com.alibaba.fastjson.JSONObject;
import org.apache.commons.lang3.StringUtils;
import org.apache.http.Consts;
import org.apache.http.HttpEntity;
import org.apache.http.HttpStatus;
import org.apache.http.NameValuePair;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.config.Registry;
import org.apache.http.config.RegistryBuilder;
import org.apache.http.conn.socket.ConnectionSocketFactory;
import org.apache.http.conn.socket.PlainConnectionSocketFactory;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.conn.ssl.TrustStrategy;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.ssl.SSLContextBuilder;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.URLEncoder;
import java.security.KeyManagementException;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class HttpClientUtils {
	public static final Logger LOG = LoggerFactory.getLogger(HttpClientUtils.class);
	
	private static SSLConnectionSocketFactory sslConnectionSocketFactory;
	private static PoolingHttpClientConnectionManager poolingHttpClientConnectionManager;
	
	private static final String CHARACTER_ENCODING = "UTF-8";

	public static final int DEFAULT_CONNECTION_TIMEOUT = 10000;
	public static final int DEFAULT_SOCKET_TIMEOUT = 2*60*1000;

	static {
		LOG.info("init connection pool");
		try {
			SSLContextBuilder sslContextBuilder = new SSLContextBuilder().loadTrustMaterial(null, new TrustStrategy() {
	             @Override
	             public boolean isTrusted(X509Certificate[] x509Certificates, String s) throws CertificateException {
	            	 //	                 信任所有站点 直接返回true
	                 return true;
	             }
	         });
			sslConnectionSocketFactory = new SSLConnectionSocketFactory(sslContextBuilder.build(), new String[]{"SSLv2Hello", "SSLv3", "TLSv1", "TLSv1.2"}, null, NoopHostnameVerifier.INSTANCE);
			Registry<ConnectionSocketFactory> registryBuilder = RegistryBuilder.<ConnectionSocketFactory>create()
	                 .register("http", PlainConnectionSocketFactory.getSocketFactory())
	                 .register("https", sslConnectionSocketFactory)
	                 .build();
			poolingHttpClientConnectionManager = new PoolingHttpClientConnectionManager(registryBuilder);
			} catch (NoSuchAlgorithmException e) {
				LOG.error("NoSuchAlgorithmException:",e);
			} catch (KeyStoreException e) {
				LOG.error("KeyStoreException:",e);
			} catch (KeyManagementException e) {
				LOG.error("KeyManagementException:",e);
			}
	}
	
	private static CloseableHttpClient getConnection() {
		CloseableHttpClient httpClient = HttpClients.custom().setSSLSocketFactory(sslConnectionSocketFactory)
				  .setConnectionManager(poolingHttpClientConnectionManager)
              .setConnectionManagerShared(true)
              .build();
		return httpClient;
	}

	/**
	 *
	 * @param connectTimeout 连接超时时间：毫秒
	 * @param socketTimeout socket超时时间：毫秒
	 * @return
	 */
	private static CloseableHttpClient getConnection(int connectTimeout,int socketTimeout) {
		RequestConfig requestConfig = RequestConfig.custom()
										.setConnectTimeout(connectTimeout)
										.setSocketTimeout(socketTimeout).build();

		CloseableHttpClient httpClient = HttpClients.custom().setSSLSocketFactory(sslConnectionSocketFactory)
				.setConnectionManager(poolingHttpClientConnectionManager)
				.setDefaultRequestConfig(requestConfig)
				.setConnectionManagerShared(true)
				.build();
		return httpClient;
	}

	public static String doGet(String url, Map<String, String> params, int connectionTimeout,int socketTimeout) throws Exception {
		CloseableHttpClient httpClient = getConnection(connectionTimeout,socketTimeout);
		return requstGet(url,params,httpClient);
	}
	
	public static String doGet(String url, Map<String, String> params) throws Exception {
		return requstGet(url,params,getConnection());
	}
	
	private static String requstGet(String url, Map<String, String> params,CloseableHttpClient httpClient) throws Exception{
		if(null!=params && params.size()>0){
			if(0 > url.indexOf("?")){
				url += "?";
			}

			for(Map.Entry<String, String> entry : params.entrySet()){
				if(StringUtils.endsWith(url, "?")) {
					url += entry.getKey()+"="+URLEncoder.encode(entry.getValue(), "UTF-8");
				}else {
					url += "&"+entry.getKey()+"="+URLEncoder.encode(entry.getValue(), "UTF-8");
				}
			}
		}

		HttpGet httpGet = new HttpGet(url);
//        RequestConfig requestConfig = RequestConfig.custom().setSocketTimeout(socketTimeout).setConnectTimeout(connectTimeout).build();
//        httpGet.setConfig(requestConfig);
		try {
			// 执行get请求.
			CloseableHttpResponse response = httpClient.execute(httpGet);
			try {
				// 获取响应实体
				int status = response.getStatusLine().getStatusCode();
				if (status == HttpStatus.SC_OK) {
					HttpEntity entity = response.getEntity();
					if (entity != null) {
						return EntityUtils.toString(entity, CHARACTER_ENCODING);
					}
				}else{
					throw new Exception("request error, http code is "+status);
				}
			} finally {
				response.close();
			}
		} catch (Exception e) {
			LOG.error("do http get error, url={}", url, e);
			throw e;
		} finally {
			// 关闭连接,释放资源
			try {
				httpGet.abort();
				httpClient.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

		return null;
	}
	


	public static String doPostJson(String url, String entity, String appToken) {
        HttpPost post = new HttpPost(url);
        String type = "application/json";
        post.setHeader("Content-Type", type);
        post.setHeader("Accept", type);
        if (!StringUtils.isBlank(appToken)) {
			post.setHeader("hg-token", appToken);
		}
        post.setEntity(new StringEntity(entity, Consts.UTF_8));
        return sendRequest(post);
    }

	public static String doPostForm(String url, Map<String, Object> formData) {
		HttpPost post = new HttpPost(url);
		List<NameValuePair> list =  new ArrayList<>();
		for (Map.Entry<String, Object> entry: formData.entrySet()) {
			list.add(new BasicNameValuePair(entry.getKey(), String.valueOf(entry.getValue())));
		}
		HttpEntity entity = new UrlEncodedFormEntity(list,Consts.UTF_8);
		post.setEntity(entity);
		return sendRequest(post);
	}
	
	private static String sendRequest(HttpUriRequest request) {
		String response;
		CloseableHttpResponse res = null;
		CloseableHttpClient client = getConnection();
		try {
			res = client.execute(request);
			HttpEntity entity = res.getEntity();
			response = EntityUtils.toString(entity,CHARACTER_ENCODING);
		} catch (Exception e) {
			LOG.error("http server error, url = {}", request.getURI(), e);
			throw new RuntimeException(e);
		} finally {
			if (res != null) {
				try {
					res.close();
				} catch (IOException e) {
					LOG.error("response close exception:",e);
				}
			}
		}
		return response;
	}


	public static String doPostOpenApi(String url, String entity, String type) throws UnsupportedEncodingException {

		HttpPost post = new HttpPost(url);

		if(StringUtils.isNotBlank(type)) {
			post.setHeader("Content-Type", type);
			post.setHeader("Accept", type);
		}

		post.setEntity(new StringEntity(entity, Consts.UTF_8));

		return sendOpenApiRequest(post);
	}

	private static String sendOpenApiRequest(HttpUriRequest request) {

		String response = null;
		CloseableHttpResponse res = null;
		CloseableHttpClient client = getConnection();
		try {
			res = client.execute(request);
			if (res.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				HttpEntity entity = res.getEntity();
				response = EntityUtils.toString(entity,CHARACTER_ENCODING);
			} else {
				HttpEntity entity = res.getEntity();
				response = EntityUtils.toString(entity,CHARACTER_ENCODING);
				throw new RuntimeException("bad Request.The request URL is invalid,response="+res.getStatusLine().getStatusCode() + response);
			}
		} catch (Exception e) {
			LOG.error("http server error, url={}", request.getURI(), e);
			throw new RuntimeException(e);
		} finally {
			if (res != null) {
				try {
					res.close();
				} catch (IOException e) {
					LOG.error("response close exception:",e);
				}
			}
		}
		return response;
	}
	
	public static void main(String[] args){
		/*String params = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?co=&resource_id=6006&query=112.65.125.218";
		HttpClientUtils http = new HttpClientUtils();
		try {
			String result = http.doGet(params, "{}");
			System.out.println(result);
		} catch (Exception e) {
			e.printStackTrace();
		}*/
		String json = "{\n" +
				"    \"code\": 400,\n" +
				"    \"msg\": \"值重复\"\n" +
				"}";
		ResponseEntity<Integer> responseEntity = JSONObject.parseObject(json, ResponseEntity.class);
		System.out.println(responseEntity.getResult());
	}
}
