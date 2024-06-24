import com.alibaba.fastjson.JSONObject;
import com.shakespeare.action.Result;
import com.shakespeare.action.collection.DeleteCollectionElement;
import com.shakespeare.action.collection.DeleteCollectionElementV2;
import org.testng.annotations.Test;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 下午2:48
 */
public class DeleteCollectionElementV2Test {

    @Test
    public void testDeleteCollectionElement(){
        DeleteCollectionElementV2 deleteCollectionElement = new DeleteCollectionElementV2();
        String params = "{\"collectionName\":\"test_2_33\",\"value\":\"192.168.1.20\"}";
        JSONObject jsonObject = JSONObject.parseObject(params);
        JSONObject config = new JSONObject();
        config.put("appToken", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ4dWhvbmdyb25nIiwic3ViIjoiT3BlbkFQSSBvZiB3dXpoaS1haS5jb20iLCJhcHBJZCI6NTE0MTg5NzA2NjgwODQ4OCwiaXNzIjoid3V6aGktYWkuY29tIiwiZXhwIjoxNjMwMzI2NTcxLCJpYXQiOjE2MzAzMjI5NzF9.CFIizQXNTnq1Nz-k148qu5ULAjOEp-IbabjTkp3jjQo");
        config.put("serverAddress", "http://mgmt.sp.com:9100");
        Result result = deleteCollectionElement.invoke(jsonObject, config);
        System.out.print(JSONObject.toJSONString(result));
    }
}
