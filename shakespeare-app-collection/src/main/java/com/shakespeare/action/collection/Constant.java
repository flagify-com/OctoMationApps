package com.shakespeare.action.collection;

/**
 * @author: hongrongxu
 * @date: 2021/5/11 上午10:54
 */
public interface Constant {

    /**
     * 添加集合api
     */
    String ADD_COLLECTION_API = "/api/collection";

    /**
     * 统计集合id添加集合元素
     */
    String API_COLLECTION_ELEMENT = "/api/collectionElement";

    /**
     * 查询元素
     */
    String API_QUERY_COLLECTION_ELEMENT  = "/api/collectionElement/find?page=1&size=10";

    /**
     * 通过ID删除集合元素
     */
    String API_DELETE_COLLECTION_ELEMENT_BY_ID = "/api/collectionElement/delete/%s";

    /**
     * 删除集合元素
     */
    String API_DELETE_COLLECTION_ELEMENT = "/api/collectionElement/deleteElement";

    /**
     * 如果没有执行人，则设置为wubaobao
     */
    String ROBOT = "wubaobao";
}
