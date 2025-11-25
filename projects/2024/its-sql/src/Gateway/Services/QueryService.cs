using Shared;

namespace Gateway.Services;

public class QueryService()
{
    public string? GetPartitionKeyValue(Node node, string partitionKeyPath)
    {
        if (node is QueryNode { Where: not null } queryNode)
        {
            return RunWhereClause(queryNode.Where.Node, partitionKeyPath);
        }

        throw new Exception("Unknown node type");
    }

    private string? RunWhereClause(Node whereClauseNode, string partitionKeyPath)
    {
        if (whereClauseNode is ComparisonNode comparisonNode)
        {
            return RunComparison(comparisonNode, partitionKeyPath);
        }

        if (whereClauseNode is LogicalNode logicalNode)
        {
            return RunLogical(logicalNode, partitionKeyPath);
        }

        throw new Exception("Unknown where clause node type");
    }

    private string? RunLogical(LogicalNode logicalNode, string partitionKeyPath)
    {
        var leftResult = RunWhereClause(logicalNode.Left, partitionKeyPath);
        if (leftResult != null)
        {
            return leftResult;
        }

        return RunWhereClause(logicalNode.Right, partitionKeyPath);
    }

    private string? RunComparison(ComparisonNode comparisonNode, string partitionKeyPath)
    {
        var column = comparisonNode.Column.Identifier;
        var value = comparisonNode.Value;

        if (value is StringValueNode stringValueNode)
        {
            return RunStringComparison(comparisonNode, partitionKeyPath, column, stringValueNode.Value);
        }

        if (value is NumberValueNode)
        {
            return null;
        }

        throw new Exception("Unknown comparison operation");
    }

    private string? RunStringComparison(ComparisonNode comparisonNode, string partitionKeyPath, string column,
        string value)
    {
        if (column == partitionKeyPath && comparisonNode.Operation == ComparisonOperation.Equal)
        {
            return value;
        }

        return null;
    }
}