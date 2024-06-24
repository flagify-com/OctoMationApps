import com.alibaba.fastjson.JSONObject;
import com.shakespeare.action.Result;
import com.shakespeare.action.collection.AddCollection;
import com.shakespeare.action.collection.AddCollectionElement;
import org.testng.annotations.Test;

/**
 * @author: hongrongxu
 * @date: 2021/5/7 下午2:48
 */
public class AddCollectionTest {

    @Test
    public void testAddCollection(){
        AddCollection addCollection = new AddCollection();
        String params = "{\"name\":\"test_2_33\",\"cnName\":\"测试集合\",\"ttl\":315360000}";
        JSONObject jsonObject = JSONObject.parseObject(params);
        JSONObject config = new JSONObject();
        config.put("appToken", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ4dWhvbmdyb25nIiwic3ViIjoiT3BlbkFQSSBvZiB3dXpoaS1haS5jb20iLCJhcHBJZCI6NTE0MTg5NzA2NjgwODQ4OCwiaXNzIjoid3V6aGktYWkuY29tIiwiZXhwIjoxNjMwMzI2NTcxLCJpYXQiOjE2MzAzMjI5NzF9.CFIizQXNTnq1Nz-k148qu5ULAjOEp-IbabjTkp3jjQo");
        config.put("serverAddress", "http://mgmt.sp.com:9100");
        Result result = addCollection.invoke(jsonObject, config);
        System.out.print(JSONObject.toJSONString(result.getData()));
    }

    @Test
    public void testAddCollectionAddEffectiveTime(){
        AddCollection addCollection = new AddCollection();
        String params = "{\"name\":\"test_2_33\",\"cnName\":\"测试集合\",\"ttl\":315360000,\"effectiveTime\":\"2022-03-02 12:00:00\"}";
        JSONObject jsonObject = JSONObject.parseObject(params);
        JSONObject config = new JSONObject();
        config.put("appToken", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ4dWhvbmdyb25nIiwic3ViIjoiT3BlbkFQSSBvZiB3dXpoaS1haS5jb20iLCJhcHBJZCI6NTE0MTg5NzA2NjgwODQ4OCwiaXNzIjoid3V6aGktYWkuY29tIiwiZXhwIjoxNjMwMzI2NTcxLCJpYXQiOjE2MzAzMjI5NzF9.CFIizQXNTnq1Nz-k148qu5ULAjOEp-IbabjTkp3jjQo");
        config.put("serverAddress", "http://mgmt.sp.com:9100");
        Result result = addCollection.invoke(jsonObject, config);
        System.out.print(JSONObject.toJSONString(result.getData()));
    }
}
